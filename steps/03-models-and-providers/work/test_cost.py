"""Checks for cost.py with the numbers from Anthropic's pricing page. No API key needed.

Run from the work folder:  python test_cost.py
"""
from math import isclose

from cost import Price, load_prices, monthly_cost, request_cost

# Opus 5.5 from the pricing page (snapshot 2026-11-13)
OPUS = Price("Claude Opus 5.5", input_per_mtok=4.0, output_per_mtok=20.0, cache_hit_per_mtok=0.20)


def test_anthropic_worked_example():
    # Pricing page p.15: 50,000 input + 15,000 output on Opus 5.5 = $0.20 + $0.30 (without the $0.08 runtime)
    assert isclose(request_cost(OPUS, 50_000, 15_000), 0.50)


def test_anthropic_worked_example_with_cache():
    # Pricing page p.16: 40,000 of the 50,000 input are cache reads = $0.04 + $0.008 + $0.30
    assert isclose(request_cost(OPUS, 50_000, 15_000, cached_tokens=40_000), 0.348)


def test_batch_is_half_price():
    assert isclose(request_cost(OPUS, 50_000, 15_000, batch=True), 0.25)


def test_batch_and_cache_stack():
    assert isclose(request_cost(OPUS, 50_000, 15_000, cached_tokens=40_000, batch=True), 0.174)


def test_cached_bigger_than_input_is_an_error():
    try:
        request_cost(OPUS, 1_000, 100, cached_tokens=2_000)
    except ValueError:
        pass
    else:
        raise AssertionError("cached_tokens > input_tokens should raise ValueError")


def test_monthly_is_one_request_times_volume():
    # 50,000 in / 15,000 out = $0.50, x 10 a day x 30 days = $150; with 80% cached = $0.348 x 300
    assert isclose(monthly_cost(OPUS, 50_000, 15_000, requests_per_day=10), 150.0)
    assert isclose(monthly_cost(OPUS, 50_000, 15_000, 10, cached_ratio=0.8), 0.348 * 300)


def test_prices_file_matches_the_docs():
    opus = next(p for p in load_prices() if p.name == "Claude Opus 5.5")
    assert opus == OPUS


if __name__ == "__main__":
    tests = [f for name, f in dict(globals()).items() if name.startswith("test_")]
    for test in tests:
        test()
        print(f"OK  {test.__name__}")
    print(f"\n{len(tests)} tests passed")
