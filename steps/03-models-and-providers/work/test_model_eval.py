"""Quick checks for score() in experiments/model_eval.py. No Ollama needed.

Run from the work folder:  python test_model_eval.py
"""
from experiments.model_eval import Receipt, normalize_name, score

EXPECTED = {
    "vendor": "Nile Stationery",
    "vendor_aliases": ["مكتبة النيل"],
    "date": "2026-11-07",
    "total": 1250.0,
    "currency": "EGP",
}


def receipt(**changes) -> Receipt:
    """A fully correct prediction, with some fields changed."""
    fields = {"vendor": "Nile Stationery", "date": "2026-11-07", "total": 1250.0, "currency": "EGP"}
    return Receipt(**(fields | changes))


def test_all_right():
    assert score(receipt(), EXPECTED) == {"vendor": True, "date": True, "total": True, "currency": True}


def test_none_means_all_wrong():
    assert score(None, EXPECTED) == {"vendor": False, "date": False, "total": False, "currency": False}


def test_vendor_ignores_case_spaces_and_punctuation():
    assert score(receipt(vendor="  NILE   stationery. "), EXPECTED)["vendor"]


def test_vendor_alias_and_arabic_letter_variants():
    assert score(receipt(vendor="مكتبه النيل"), EXPECTED)["vendor"]  # ه instead of ة


def test_vendor_partial_name_is_wrong():
    assert not score(receipt(vendor="Nile"), EXPECTED)["vendor"]


def test_date_format_matters():
    assert not score(receipt(date="07/11/2026"), EXPECTED)["date"]
    assert not score(receipt(date="2026-11-7"), EXPECTED)["date"]
    assert score(receipt(date=" 2026-11-07 "), EXPECTED)["date"]


def test_total_tolerance():
    assert score(receipt(total=1250), EXPECTED)["total"]  # 1250 vs 1250.0
    assert score(receipt(total=1250.004), EXPECTED)["total"]
    assert not score(receipt(total=1250.5), EXPECTED)["total"]
    assert not score(receipt(total=1.25), EXPECTED)["total"]  # thousands separator read as decimal


def test_currency_case_but_not_symbols():
    assert score(receipt(currency="egp"), EXPECTED)["currency"]
    assert not score(receipt(currency="LE"), EXPECTED)["currency"]


def test_normalize_name():
    assert normalize_name("El-Salam") == "el salam"
    assert normalize_name("أبو  حسن") == "ابو حسن"


if __name__ == "__main__":
    tests = [f for name, f in dict(globals()).items() if name.startswith("test_")]
    for test in tests:
        test()
        print(f"OK  {test.__name__}")
    print(f"\n{len(tests)} tests passed")
