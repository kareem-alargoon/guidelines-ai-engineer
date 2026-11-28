"""Task 7: what would the receipts idea cost on the Claude API?

Run from the work folder:  python cost.py
"""
import json
from dataclasses import dataclass
from pathlib import Path

PRICES_FILE = Path(__file__).parent / "data" / "prices.json"


@dataclass
class Price:
    name: str
    input_per_mtok: float
    output_per_mtok: float
    cache_hit_per_mtok: float


def load_prices(path: Path = PRICES_FILE) -> list[Price]:
    """Read prices.json and keep only the fields cost.py needs."""
    data = json.loads(path.read_text(encoding="utf-8"))
    return [
        Price(
            name=m["name"],
            input_per_mtok=m["input_per_mtok"],
            output_per_mtok=m["output_per_mtok"],
            cache_hit_per_mtok=m["cache_hit_per_mtok"],
        )
        for m in data["models"]
    ]


MTOK = 1_000_000
BATCH_DISCOUNT = 0.5  # Batch API = 50% off input and output (pricing page p.7)


def request_cost(price: Price, input_tokens: int, output_tokens: int,
                 cached_tokens: int = 0, batch: bool = False) -> float:
    """Dollar cost of one request.

    cached_tokens is PART of input_tokens (the API counts them inside the input):
    that part pays the cache hit price, the rest pays the normal input price.
    batch=True halves everything, cache hits too (the discounts stack, p.6 + FAQ).
    """
    if min(input_tokens, output_tokens, cached_tokens) < 0:
        raise ValueError("token counts can't be negative")
    if cached_tokens > input_tokens:
        raise ValueError(f"cached_tokens ({cached_tokens}) is part of input_tokens ({input_tokens}), "
                         "so it can't be bigger")

    uncached = input_tokens - cached_tokens
    cost = (uncached * price.input_per_mtok
            + cached_tokens * price.cache_hit_per_mtok
            + output_tokens * price.output_per_mtok) / MTOK
    return cost * BATCH_DISCOUNT if batch else cost


def monthly_cost(price: Price, avg_input: float, avg_output: float, requests_per_day: int,
                 days: int = 30, cached_ratio: float = 0.0, batch: bool = False) -> float:
    """Cost of an average request x requests per day x days.

    cached_ratio = share of the input that repeats in every request (e.g. the system prompt).
    """
    if not 0 <= cached_ratio <= 1:
        raise ValueError("cached_ratio must be between 0 and 1")
    # request_cost takes ints, but averages are floats: the math is the same, so pass them through
    one = request_cost(price, avg_input, avg_output, cached_tokens=avg_input * cached_ratio, batch=batch)
    return one * requests_per_day * days


# ---------- the receipts idea ----------
EVAL_FILE = Path(__file__).parent / "experiments" / "results" / "model_eval.json"
LOCAL_MODEL = "qwen2.5:3b"
RECEIPTS_PER_DAY = 80   # 200 employees x ~2 receipts a week / 5 work days (use_case.md)
WORK_DAYS = 22          # receipts come on work days, not 30 days a month
CACHED_RATIO = 0.5      # system prompt ~172 of 330.5 tokens (Qwen tokenizer, measured on Ollama)


def load_local_result(path: Path = EVAL_FILE, model: str = LOCAL_MODEL) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    return next(m["summary"] for m in data["models"] if m["model"] == model)


def main() -> None:
    local = load_local_result()
    avg_in, avg_out = local["avg_input_tokens"], local["avg_output_tokens"]
    monthly = RECEIPTS_PER_DAY * WORK_DAYS

    print(f"Receipts: {RECEIPTS_PER_DAY}/day x {WORK_DAYS} work days = {monthly:,}/month")
    print(f"Average tokens per receipt (from Task 6, {LOCAL_MODEL}): {avg_in} in / {avg_out} out")
    print(f"Prices: Anthropic snapshot 2026-11-13. Cache = system prompt ({CACHED_RATIO:.0%} of input)\n")

    header = f"{'Model':<18} {'$/receipt':>10} {'normal':>9} {'batch':>9} {'cache':>9} {'batch+cache':>12}"
    print(header + "   ($ per month)")
    print("-" * len(header))
    for p in load_prices():
        def month(cached_ratio: float = 0.0, batch: bool = False) -> float:
            return monthly_cost(p, avg_in, avg_out, RECEIPTS_PER_DAY, WORK_DAYS, cached_ratio, batch)

        per_receipt = request_cost(p, avg_in, avg_out)
        print(f"{p.name.removeprefix('Claude '):<18} {per_receipt:>10.6f} {month():>9.2f} "
              f"{month(batch=True):>9.2f} {month(CACHED_RATIO):>9.2f} {month(CACHED_RATIO, True):>12.2f}")

    compute_minutes = local["avg_latency_seconds"] * RECEIPTS_PER_DAY / 60
    print(f"{'Local ' + LOCAL_MODEL:<18} {0:>10.6f} {0:>9.2f}   <- $0 per request, but NOT counted here:")
    print(f"  - the machine itself (desktop, CPU only), electricity, updates and someone who maintains it")
    print(f"  - speed: {local['avg_latency_seconds']} s/receipt on CPU = ~{compute_minutes:.0f} min of compute a day "
          f"(fine for a background job)")
    print(f"  - license: {local['license']} = non-commercial. A commercial app needs another model (Task 6)")

    print("\n[!] Estimate, not an invoice: these token counts come from the Qwen tokenizer.")
    print("    Claude counts tokens with its own tokenizer (newer models ~30% more tokens, pricing p.2).")
    print("[!] 'cache' assumes the system prompt gets cached. Prompt caching has a minimum prompt length;")
    print("    check it in the prompt caching docs (Step 04). Our ~172-token system prompt may be too short.")
    print("[!] Data: real receipts are personal/financial data. Cloud only with fake or masked receipts (use_case.md).")


if __name__ == "__main__":
    main()
