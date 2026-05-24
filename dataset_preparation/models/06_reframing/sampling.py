import numpy as np
import pandas as pd
from prompts import Example

GLOBAL_SEED = 42

def _train_thought_pool(train_df: pd.DataFrame) -> pd.DataFrame:
    """
    Collapse train to one row per thought_id (first reframe).
    The few-shot examples are drawn from this collapsed pool to enforce
    thought_id uniqueness within a prompt.
    """
    return (
        train_df
        .drop_duplicates(subset="thought_id", keep="first")
        .reset_index(drop=True)
    )


def _row_to_example(row: pd.Series) -> Example:
    return Example(
        situation=row["situation"],
        thought=row["thought"],
        reframe=row["reframe"],
        category=row["category"],
    )


def sample_random_examples(
    pool: pd.DataFrame,
    test_thought_id: int,
    n: int = 3,
    salt: str = "random",
) -> list[Example]:
    """
    Sample n examples uniformly at random from the (unique-thought) pool.
    Seeded by (GLOBAL_SEED, test_thought_id, salt) for reproducibility.
    """
    seed = hash((GLOBAL_SEED, test_thought_id, salt)) % (2**32)
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(pool), size=n, replace=False)
    return [_row_to_example(pool.iloc[i]) for i in idx]


def sample_category_examples(
    pool: pd.DataFrame,
    test_thought_id: int,
    category: str,
    n: int = 3,
    salt: str = "category",
) -> tuple[list[Example], str]:
    """
    Sample n examples whose category matches `category`. If fewer than n
    category-matched examples are available in the pool, fall back to
    random sampling for the remaining slots.

    Returns (examples, fallback_status) where fallback_status is one of:
      "exact"  - all n examples are category-matched
      "partial:k" - k category-matched + (n-k) random
    """
    seed = hash((GLOBAL_SEED, test_thought_id, salt)) % (2**32)
    rng = np.random.default_rng(seed)

    matched = pool[pool["category"] == category]

    if len(matched) >= n:
        idx = rng.choice(len(matched), size=n, replace=False)
        examples = [_row_to_example(matched.iloc[i]) for i in idx]
        return examples, "exact"

    # Partial fallback: take all matched, fill the rest from non-matched
    matched_examples = [_row_to_example(matched.iloc[i]) for i in range(len(matched))]
    deficit = n - len(matched)
    non_matched = pool[pool["category"] != category]
    fill_idx = rng.choice(len(non_matched), size=deficit, replace=False)
    fill_examples = [_row_to_example(non_matched.iloc[i]) for i in fill_idx]

    return matched_examples + fill_examples, f"partial:{len(matched)}"