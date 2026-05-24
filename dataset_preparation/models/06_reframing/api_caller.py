import time
from prompts import DECODING_PARAMS, MODEL, SYSTEM_MESSAGE

def call_api(client, prompt, max_retries = 3):
    """
    Fire a single API call. Returns a dict with text, usage, latency.
    Retries with exponential backoff on transient errors.
    """
    for attempt in range(max_retries):
        try:
            t0 = time.perf_counter()
            response = client.messages.create(
                model=MODEL,
                max_tokens=DECODING_PARAMS["max_tokens"],
                system=SYSTEM_MESSAGE,
                messages=[{"role": "user", "content": prompt}],
            )
            latency_ms = (time.perf_counter() - t0) * 1000

            return {
                "text": response.content[0].text.strip(),
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "latency_ms": round(latency_ms, 1),
                "error": None,
            }
        except Exception as e:
            if attempt < max_retries - 1:
                wait = 2 ** attempt
                print(f"  retry {attempt + 1}/{max_retries} after {wait}s: {type(e).__name__}: {e}")
                time.sleep(wait)
            else:
                return {
                    "text": "",
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "latency_ms": 0,
                    "error": f"{type(e).__name__}: {e}",
                }