"""Read the saved Artificial Analysis "API Providers" snapshot and query it.

The page was saved as text, so every table row is spread over 13 lines:

    0  "<Provider> logo"     (noise)
    1  provider
    2  "<Provider> logo"     (noise)
    3  model
    4  intelligence index    "65" or "--"
    5  cost per task         "$26.54" or "--"
    6  time per task (min)   "46.8" or "--"
    7  first answer token s  "267.23" or "--"
    8  error rate            "5.7%" or "--"
    9  context               "1M", "131k"
    10 license               "Open" or "Proprietary"
    11 "Model"               (noise: a button on the page)
    12 "Provider"            (noise: a button on the page)

The table starts right after the "Further Analysis" line and ends when the
next line is no longer a "... logo" line ("Key definitions").
"""

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

# work/ -> 03-models-and-providers/ -> steps/ -> repo root
REPO_ROOT = Path(__file__).resolve().parents[3]
PROVIDERS_FILE = REPO_ROOT / "resources" / "articles" / "03-artificial-analysis-providers.md"
SNAPSHOT_DATE = "2026-11-13"

ROW_SIZE = 13
TABLE_START_MARKER = "Further Analysis"
MISSING = "--"

# Tags a provider adds to the model name for ITS deployment (speed tier,
# quantization, platform). Same weights underneath -> same model.
# Reasoning effort ("max", "high", "non-reasoning") is NOT here on purpose:
# it changes the intelligence index, so it counts as a different model.
# Collected from this snapshot; a newer snapshot may add new tags.
PROVIDER_TAGS = {
    "FAST", "ULTRA", "ULTRA CHAT", "FP4 ULTRA CHAT", "ULTRAFAST", "FLEX",
    "TURBO", "BASE", "VERTEX", "AI STUDIO", "HIGH SPEED",
    "BF16", "FP8", "MXFP8", "FP4", "NVFP4",
}
# Some providers append a tag WITHOUT parentheses ("gpt-oss-120b (high) Vertex").
# Kept smaller on purpose: "Ultra" is part of real names ("Nemotron 3 Ultra").
BARE_PROVIDER_TAGS = {"VERTEX", "AI STUDIO", "BASE", "HIGH SPEED", "BF16", "FP8"}

# The two models compared in section 3 of the report.
PROPRIETARY_PICK = "Claude Opus 5.5 (max)"
OPEN_PICK = "gpt-oss-120b (high)"


@dataclass
class Endpoint:
    provider: str
    model: str
    intelligence: int | None
    cost_per_task: float | None       # "$1.27" -> 1.27 , "--" -> None
    time_per_task_min: float | None
    first_answer_token_s: float | None
    error_rate: float | None          # "5.7%" -> 5.7
    context: str                      # kept as text: "1M", "131k"
    license: str                      # "Open" or "Proprietary"


# ---------- parsing ----------

def _to_float(text: str) -> float | None:
    """'$1,027.50' / '5.7%' / '46.8' -> float, '--' -> None."""
    if text == MISSING:
        return None
    return float(text.replace("$", "").replace(",", "").replace("%", ""))


def _to_int(text: str) -> int | None:
    return None if text == MISSING else int(text)


def _parse_row(row: list[str]) -> Endpoint:
    return Endpoint(
        provider=row[1],
        model=row[3],
        intelligence=_to_int(row[4]),
        cost_per_task=_to_float(row[5]),
        time_per_task_min=_to_float(row[6]),
        first_answer_token_s=_to_float(row[7]),
        error_rate=_to_float(row[8]),
        context=row[9],
        license=row[10],
    )


def _check_row(row: list[str], line_no: int) -> None:
    """Fail loudly if the 13-line pattern breaks, instead of reading garbage."""
    ok = (
        len(row) == ROW_SIZE
        and row[0].endswith(" logo")
        and row[2].endswith(" logo")
        and row[11] == "Model"
        and row[12] == "Provider"
        and row[10] in ("Open", "Proprietary")
    )
    if not ok:
        raise ValueError(f"Unexpected row shape near line {line_no}: {row}")


def load_endpoints(path: Path) -> list[Endpoint]:
    lines = path.read_text(encoding="utf-8").splitlines()
    i = lines.index(TABLE_START_MARKER) + 1

    endpoints: list[Endpoint] = []
    # A new row always starts with a "... logo" line; anything else = table ended.
    while i < len(lines) and lines[i].endswith(" logo"):
        row = lines[i : i + ROW_SIZE]
        _check_row(row, line_no=i + 1)
        endpoints.append(_parse_row(row))
        i += ROW_SIZE
    return endpoints


# ---------- model names ----------

def _is_provider_tag(text: str) -> bool:
    """'FAST' -> True, 'FP4, FAST' -> True, 'max' -> False."""
    return all(part.strip().upper() in PROVIDER_TAGS for part in text.split(","))


def base_model(name: str) -> str:
    """Strip provider tags from the END of a model name.

    'Kimi K3.1 Pro (FAST)'            -> 'Kimi K3.1 Pro'
    'GLM-5.3 (max) (FP4, FAST)'       -> 'GLM-5.3 (max)'
    'gpt-oss-120b (high) Vertex'      -> 'gpt-oss-120b (high)'
    'Kimi K3.1 Pro High Speed'        -> 'Kimi K3.1 Pro'
    'Claude Opus 5.5 (max)'           -> unchanged ('max' is reasoning effort)
    """
    name = name.strip()
    while True:
        if name.endswith(")") and "(" in name:
            inner_start = name.rindex("(")
            if _is_provider_tag(name[inner_start + 1 : -1]):
                name = name[:inner_start].rstrip()
                continue
        last_words = [t for t in BARE_PROVIDER_TAGS if name.upper().endswith(" " + t)]
        if last_words:
            name = name[: -len(max(last_words, key=len))].rstrip()
            continue
        return name


# ---------- queries ----------

def top_models(
    endpoints: list[Endpoint], n: int = 10, license: str | None = None
) -> list[Endpoint]:
    """Best n *distinct* models by intelligence.

    A model is counted once, no matter how many providers (or provider-tagged
    variants like "(FAST)") serve it. The returned endpoint is just a sample.
    """
    candidates = [
        e for e in endpoints
        if e.intelligence is not None and (license is None or e.license == license)
    ]
    candidates.sort(key=lambda e: e.intelligence, reverse=True)

    seen: set[str] = set()
    result: list[Endpoint] = []
    for e in candidates:
        key = base_model(e.model)
        if key in seen:
            continue
        seen.add(key)
        result.append(e)
        if len(result) == n:
            break
    return result


def providers_for(
    endpoints: list[Endpoint], model: str, include_variants: bool = False
) -> list[Endpoint]:
    """All endpoints of one model, cheapest first, unknown cost last.

    include_variants=False: exact name only.
    include_variants=True : also provider-tagged names ("... (Turbo)", "... Vertex").
    """
    if include_variants:
        wanted = base_model(model)
        matches = [e for e in endpoints if base_model(e.model) == wanted]
    else:
        matches = [e for e in endpoints if e.model == model]
    return sorted(
        matches,
        key=lambda e: (e.cost_per_task is None, e.cost_per_task or 0.0),
    )


def count_by_license(endpoints: list[Endpoint]) -> dict[str, int]:
    counts: defaultdict[str, int] = defaultdict(int)
    for e in endpoints:
        counts[e.license] += 1
    return dict(counts)


def endpoints_per_model(endpoints: list[Endpoint]) -> dict[str, int]:
    """base model name -> number of endpoints (all providers and variants)."""
    counts: defaultdict[str, int] = defaultdict(int)
    for e in endpoints:
        counts[base_model(e.model)] += 1
    return dict(counts)


# ---------- printing ----------

def _fmt(value: float | int | None, prefix: str = "", suffix: str = "", digits: int = 2) -> str:
    if value is None:
        return MISSING
    if isinstance(value, int):
        return f"{prefix}{value}{suffix}"
    return f"{prefix}{value:.{digits}f}{suffix}"


def print_top(title: str, models: list[Endpoint], endpoint_counts: dict[str, int]) -> None:
    names = [base_model(e.model) for e in models]
    width = max([len("Model"), *map(len, names)])
    print(f"\n{title}")
    print(f"{'#':>2}  {'Model':<{width}}  {'Index':>5}  {'License':<11} {'Endpoints':>9}")
    print("-" * (width + 34))
    for rank, (name, e) in enumerate(zip(names, models), start=1):
        print(
            f"{rank:>2}  {name:<{width}}  {e.intelligence:>5}  {e.license:<11} "
            f"{endpoint_counts[name]:>9}"
        )


def _provider_label(e: Endpoint, model: str) -> str:
    """'Google' or 'Google [Vertex]' when the endpoint name has a provider tag."""
    if e.model == model:
        return e.provider
    tag = e.model.removeprefix(model).strip(" ()")
    return f"{e.provider} [{tag}]"


def print_providers(model: str, rows: list[Endpoint]) -> None:
    exact = sum(1 for e in rows if e.model == model)
    print(
        f"\n{model}: {len(rows)} endpoints "
        f"({exact} exact name + {len(rows) - exact} provider-tagged), sorted by cost per task"
    )
    if not rows:
        print("  (no endpoint with this name)")
        return
    labels = [_provider_label(e, model) for e in rows]
    width = max([len("Provider"), *map(len, labels)])
    print(
        f"{'Provider':<{width}}  {'Cost/Task':>10} {'Time(min)':>10} "
        f"{'1st tok(s)':>11} {'Errors':>8} {'Context':>8}"
    )
    print("-" * (width + 52))
    for label, e in zip(labels, rows):
        print(
            f"{label:<{width}}  {_fmt(e.cost_per_task, prefix='$'):>10} "
            f"{_fmt(e.time_per_task_min, digits=1):>10} "
            f"{_fmt(e.first_answer_token_s, digits=1):>11} "
            f"{_fmt(e.error_rate, suffix='%', digits=1):>8} {e.context:>8}"
        )

    with_cost = [e for e in rows if e.cost_per_task is not None]
    with_time = [e for e in rows if e.time_per_task_min is not None]
    with_err = [e for e in rows if e.error_rate is not None]

    def label(e: Endpoint) -> str:
        return _provider_label(e, model)

    if with_cost:
        cheapest = min(with_cost, key=lambda e: e.cost_per_task)
        priciest = max(with_cost, key=lambda e: e.cost_per_task)
        print(f"  Cheapest:          {label(cheapest)} (${cheapest.cost_per_task:.2f})")
        # A few endpoints show "$0.00" (rounded, or free): no ratio then, instead of ZeroDivisionError.
        ratio = f"{priciest.cost_per_task / cheapest.cost_per_task:.1f}x" if cheapest.cost_per_task else "n/a ($0.00)"
        print(
            f"  Priciest/cheapest: {label(priciest)} ${priciest.cost_per_task:.2f} "
            f"/ ${cheapest.cost_per_task:.2f} = {ratio}"
        )
    if with_time:
        fastest = min(with_time, key=lambda e: e.time_per_task_min)
        print(f"  Fastest:           {label(fastest)} ({fastest.time_per_task_min:.1f} min/task)")
    if with_err:
        best = min(e.error_rate for e in with_err)
        safest = [label(e) for e in with_err if e.error_rate == best]
        print(f"  Lowest error rate: {', '.join(safest)} ({best:.1f}%)")


if __name__ == "__main__":
    endpoints = load_endpoints(PROVIDERS_FILE)
    counts = count_by_license(endpoints)
    per_model = endpoints_per_model(endpoints)
    exact_names = {e.model for e in endpoints}

    print(f"Artificial Analysis providers snapshot ({SNAPSHOT_DATE})")
    print(
        f"Endpoints: {len(endpoints)}  |  model names: {len(exact_names)}  |  "
        f"models without provider tags: {len(per_model)}"
    )
    print(f"Open: {counts.get('Open', 0)}  |  Proprietary: {counts.get('Proprietary', 0)}")

    print_top("Top 10 models (all licenses)", top_models(endpoints, 10), per_model)
    print_top("Top 10 open models", top_models(endpoints, 10, license="Open"), per_model)

    for pick in (PROPRIETARY_PICK, OPEN_PICK):
        print_providers(pick, providers_for(endpoints, pick, include_variants=True))
