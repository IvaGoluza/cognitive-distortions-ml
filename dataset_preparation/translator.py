"""
translator.py — EN -> HR translation via Google Cloud Translation API (v2 NMT).

Design goals:
  - Batched API calls (up to 50 strings per request) to amortise overhead.
  - Exponential-backoff retries on transient errors (network, 5xx, 429).
  - Incremental save: every batch is checkpointed to disk, so a crash or
    interruption never loses more than ~50 rows of work.
  - Idempotent: re-running the same job picks up where it left off based
    on what is already in the checkpoint file.
  - Dedup: identical input strings get translated once; duplicates copy
    the result. Important for Cognitive Reframing where situation/thought
    repeat across reframe rows.

Authentication:
  Cloud Translation API v2 (Basic) supports API key auth via the `key`
  query parameter. The API key is read from the GOOGLE_TRANSLATE_API_KEY
  environment variable.

References:
  Google Cloud Translation API v2 reference:
  https://cloud.google.com/translate/docs/reference/rest/v2/translate
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import requests


API_URL = "https://translation.googleapis.com/language/translate/v2"
DEFAULT_BATCH_SIZE = 50          # API supports up to 128; 50 is the safer common choice.
DEFAULT_MAX_RETRIES = 5
DEFAULT_BACKOFF_BASE = 2.0       # Seconds; doubled each retry: 2, 4, 8, 16, 32.
DEFAULT_TIMEOUT = 60             # Per-request HTTP timeout in seconds.
DEFAULT_SOURCE = "en"
DEFAULT_TARGET = "hr"


# ----------------------------------------------------------------------
# Errors
# ----------------------------------------------------------------------

class TranslationError(RuntimeError):
    """Raised when the API returns a non-retryable error or retries are exhausted."""


# ----------------------------------------------------------------------
# Cache / checkpoint
# ----------------------------------------------------------------------

@dataclass
class TranslationCache:
    """
    On-disk mapping of source string → translated string. Persists across runs
    so that re-executing a job translates only what was not already translated.
    """
    path: Path
    data: dict[str, str] = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path) -> "TranslationCache":
        path = Path(path)
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return cls(path=path, data=data)
        path.parent.mkdir(parents=True, exist_ok=True)
        return cls(path=path, data={})

    def save(self) -> None:
        # Atomic write via temp file → rename, so a crash mid-save never
        # leaves a half-written cache.
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False)
        tmp.replace(self.path)

    def __len__(self) -> int:
        return len(self.data)

    def __contains__(self, key: str) -> bool:
        return key in self.data

    def get(self, key: str) -> str | None:
        return self.data.get(key)

    def update(self, mapping: dict[str, str]) -> None:
        self.data.update(mapping)


# ----------------------------------------------------------------------
# API call with retries
# ----------------------------------------------------------------------

def _translate_batch_with_retries(
    texts: list[str],
    api_key: str,
    source: str = DEFAULT_SOURCE,
    target: str = DEFAULT_TARGET,
    max_retries: int = DEFAULT_MAX_RETRIES,
    backoff_base: float = DEFAULT_BACKOFF_BASE,
    timeout: int = DEFAULT_TIMEOUT,
) -> list[str]:
    """
    Translate a single batch of strings. Retries on transient errors with
    exponential backoff. Raises TranslationError on permanent failure.

    The v2 API takes the source strings as repeated `q` parameters and
    returns translations in the same order in `data.translations`.
    """
    params = {
        "key": api_key,
        "source": source,
        "target": target,
        "format": "text",       # Disable HTML entity processing.
    }
    # `q` can be repeated to translate multiple strings in one call.
    data = [("q", t) for t in texts]

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(API_URL, params=params, data=data, timeout=timeout)
        except requests.RequestException as e:
            # Network-level error: retry.
            if attempt == max_retries:
                raise TranslationError(f"Network error after {max_retries} attempts: {e}") from e
            sleep = backoff_base ** attempt
            print(f"  [retry {attempt}/{max_retries}] network error: {e}; sleeping {sleep:.1f}s")
            time.sleep(sleep)
            continue

        if response.status_code == 200:
            payload = response.json()
            translations = payload.get("data", {}).get("translations", [])
            if len(translations) != len(texts):
                raise TranslationError(
                    f"API returned {len(translations)} translations for {len(texts)} inputs"
                )
            return [t["translatedText"] for t in translations]

        if response.status_code in (429, 500, 502, 503, 504):
            # Rate limit / transient server error: retry.
            if attempt == max_retries:
                raise TranslationError(
                    f"API returned {response.status_code} after {max_retries} attempts: {response.text}"
                )
            sleep = backoff_base ** attempt
            print(f"  [retry {attempt}/{max_retries}] HTTP {response.status_code}; sleeping {sleep:.1f}s")
            time.sleep(sleep)
            continue

        # 400, 401, 403, 404 etc — permanent.
        raise TranslationError(
            f"API returned non-retryable HTTP {response.status_code}: {response.text}"
        )

    raise TranslationError("Exhausted retries without raising — should not reach here.")


# ----------------------------------------------------------------------
# Top-level translate function
# ----------------------------------------------------------------------

def translate_strings(
    strings: Iterable[str],
    cache_path: Path,
    api_key: str | None = None,
    batch_size: int = DEFAULT_BATCH_SIZE,
    source: str = DEFAULT_SOURCE,
    target: str = DEFAULT_TARGET,
    save_every_n_batches: int = 1,
    verbose: bool = True,
) -> dict[str, str]:
    """
    Translate an iterable of strings EN → HR (by default), with on-disk
    deduplication and incremental checkpointing.

    Returns a mapping {source_string: translated_string} covering every
    unique non-empty string in `strings`. Empty / None / whitespace-only
    inputs are skipped.

    The cache file at `cache_path` is updated after each batch (or every
    `save_every_n_batches` batches) and is the source of truth for
    resumption — if you re-run the same job, only un-cached strings
    are sent to the API.
    """
    if api_key is None:
        api_key = os.environ.get("GOOGLE_TRANSLATE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_TRANSLATE_API_KEY is not set. "
            "Set it in your shell or .env file before running translation."
        )

    cache = TranslationCache.load(Path(cache_path))

    # Deduplicate, drop empty, drop already-cached.
    seen: set[str] = set()
    todo: list[str] = []
    for s in strings:
        if s is None:
            continue
        s = str(s)
        if not s.strip():
            continue
        if s in seen:
            continue
        seen.add(s)
        if s not in cache:
            todo.append(s)

    if verbose:
        print(f"  cache: {len(cache):,} entries already present")
        print(f"  inputs: {len(seen):,} unique non-empty strings")
        print(f"  to translate: {len(todo):,} strings ({len(seen) - len(todo):,} cache hits)")

    if not todo:
        if verbose:
            print("  nothing to do, returning cache as-is")
        return {s: cache.get(s) for s in seen if cache.get(s) is not None}

    total_chars = sum(len(s) for s in todo)
    if verbose:
        print(f"  total characters to send: {total_chars:,} (~${total_chars / 1e6 * 20:.2f} at $20/1M)")

    # Translate in batches.
    n_batches = (len(todo) + batch_size - 1) // batch_size
    batches_since_save = 0
    started = time.time()

    for batch_idx in range(n_batches):
        batch = todo[batch_idx * batch_size:(batch_idx + 1) * batch_size]
        translated = _translate_batch_with_retries(
            batch, api_key=api_key, source=source, target=target,
        )
        cache.update(dict(zip(batch, translated)))
        batches_since_save += 1

        if batches_since_save >= save_every_n_batches:
            cache.save()
            batches_since_save = 0

        if verbose and (batch_idx + 1) % 10 == 0:
            done = (batch_idx + 1) * batch_size
            done = min(done, len(todo))
            elapsed = time.time() - started
            rate = done / elapsed if elapsed > 0 else 0
            eta = (len(todo) - done) / rate if rate > 0 else 0
            print(f"  batch {batch_idx + 1:>4}/{n_batches}  ({done:,}/{len(todo):,})  "
                  f"elapsed {elapsed:.0f}s  eta {eta:.0f}s")

    # Final save.
    if batches_since_save > 0:
        cache.save()

    if verbose:
        elapsed = time.time() - started
        print(f"  done in {elapsed:.0f}s; cache now has {len(cache):,} entries")

    return {s: cache.get(s) for s in seen if cache.get(s) is not None}


# ----------------------------------------------------------------------
# Convenience: translate a column of a DataFrame
# ----------------------------------------------------------------------

def add_hr_column(df, source_col: str, target_col: str, translation_map: dict[str, str]):
    """
    Add a new column `target_col` to `df`, mapping each row's `source_col`
    value through `translation_map`. Empty / None / unmapped entries become
    None in the target column.
    """
    def _map(value):
        if value is None:
            return None
        s = str(value)
        if not s.strip():
            return None
        return translation_map.get(s)

    df[target_col] = df[source_col].map(_map)
    return df
