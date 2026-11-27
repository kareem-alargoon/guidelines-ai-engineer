"""Step 03, Task 3: where does the time go? Cold start vs warm, and keep_alive.

Run from the work/ folder:  python -m experiments.latency
"""
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from statistics import mean
import json
import time

from llm_client import chat, Role, ChatResult, OLLAMA_MODEL
from model_card import get_json, get_running_models, print_running_models

# Change this when you run it on the work laptop: the numbers depend on the hardware.
MACHINE = "personal desktop (i5-14600K, 32 GB DDR5, no dedicated GPU)"

PROMPT = "Explain in two sentences what a REST API is."
TEMPERATURE = 0
MAX_TOKENS = 100
COLD_RUNS = 3
WARM_RUNS = 5

RESULTS_FILE = Path(__file__).parent / "results" / "latency.json"


def unload() -> None:
    """Empty request + keep_alive=0 = unload the model now (like `ollama stop`)."""
    chat([], keep_alive=0)


def preload() -> float:
    """Empty request with no keep_alive = load the model and keep it (default 5 minutes).

    Returns the wall-clock seconds measured here: for an empty request Ollama answers
    with done_reason "load" and no load_duration, so we time it ourselves.
    """
    start = time.perf_counter()
    chat([])
    return time.perf_counter() - start


def ask(keep_alive: int | str | None = None) -> tuple[ChatResult, float]:
    """Send PROMPT once. Returns the result and the wall-clock time measured here, in Python."""
    messages = [{"role": Role.USER.value, "content": PROMPT}]
    start = time.perf_counter()
    result = chat(messages, temperature=TEMPERATURE, max_tokens=MAX_TOKENS, keep_alive=keep_alive)
    wall_seconds = time.perf_counter() - start
    return result, wall_seconds


def to_row(kind: str, run: int, result: ChatResult, wall_seconds: float) -> dict:
    return {
        "kind": kind,
        "run": run,
        "load_seconds": round(result.load_seconds, 3),
        "prompt_eval_seconds": round(result.prompt_eval_seconds, 3),
        "eval_seconds": round(result.eval_seconds, 3),
        "total_seconds": round(result.duration_seconds, 3),
        # Time until the first token shows up: load the model + read the prompt.
        # (Generating that first token adds one decode step, ~0.03 s here, so we leave it out.)
        "ttft_seconds": round(result.load_seconds + result.prompt_eval_seconds, 3),
        "input_tokens": result.input_tokens,
        "output_tokens": result.output_tokens,
        "tokens_per_second": round(result.output_tokens_per_second, 1),
        # Ollama's total + HTTP + JSON parsing, seen from Python.
        "wall_seconds": round(wall_seconds, 3),
    }


def print_table(rows: list[dict]) -> None:
    header = (
        f"{'KIND':<8}{'RUN':>4}{'LOAD':>8}{'PROMPT':>8}{'EVAL':>8}{'TOTAL':>8}"
        f"{'TTFT':>8}{'TOK/S':>8}{'OUT':>5}{'WALL':>8}"
    )
    print(header)
    print("-" * len(header))
    for row in rows:
        print(
            f"{row['kind']:<8}{row['run']:>4}{row['load_seconds']:>8.2f}{row['prompt_eval_seconds']:>8.2f}"
            f"{row['eval_seconds']:>8.2f}{row['total_seconds']:>8.2f}{row['ttft_seconds']:>8.2f}"
            f"{row['tokens_per_second']:>8.1f}{row['output_tokens']:>5}{row['wall_seconds']:>8.2f}"
        )


def averages(rows: list[dict], kind: str) -> dict:
    picked = [row for row in rows if row["kind"] == kind]
    keys = ["load_seconds", "prompt_eval_seconds", "eval_seconds", "total_seconds", "ttft_seconds",
            "tokens_per_second"]
    return {key: round(mean(row[key] for row in picked), 3) for key in keys}


def main() -> None:
    rows = []

    # Start from a known state: nothing loaded, so the first request is really cold.
    unload()

    print(f"Cold: {COLD_RUNS} requests with keep_alive=0 (the model is unloaded after each one)...")
    for run in range(1, COLD_RUNS + 1):
        result, wall = ask(keep_alive=0)
        rows.append(to_row("cold", run, result, wall))
    running_after_cold = get_running_models()  # expected: empty

    print("Preload: empty request, then the model stays loaded...")
    preload_seconds = preload()

    print(f"Warm: {WARM_RUNS} requests with the default keep_alive...")
    for run in range(1, WARM_RUNS + 1):
        result, wall = ask()
        rows.append(to_row("warm", run, result, wall))
    running_after_warm = get_running_models()

    print()
    print_table(rows)

    cold_avg = averages(rows, "cold")
    warm_avg = averages(rows, "warm")
    print()
    print(f"Average cold: total {cold_avg['total_seconds']:.2f} s, TTFT {cold_avg['ttft_seconds']:.2f} s, "
          f"load {cold_avg['load_seconds']:.2f} s, {cold_avg['tokens_per_second']:.1f} tok/s")
    print(f"Average warm: total {warm_avg['total_seconds']:.2f} s, TTFT {warm_avg['ttft_seconds']:.2f} s, "
          f"load {warm_avg['load_seconds']:.2f} s, {warm_avg['tokens_per_second']:.1f} tok/s")

    print(f"Preload (measured in Python): {preload_seconds:.2f} s")

    print()
    print(f"Running models after cold: {len(running_after_cold)}")
    print("Running models after warm (like `ollama ps`):")
    print_running_models(running_after_warm)

    report = {
        "date": datetime.now().isoformat(timespec="seconds"),
        "machine": MACHINE,
        "ollama_version": get_json("/api/version")["version"],
        "model": OLLAMA_MODEL,
        "prompt": PROMPT,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "requests": rows,
        "preload_wall_seconds": round(preload_seconds, 3),
        "averages": {"cold": cold_avg, "warm": warm_avg},
        "running_models_after_cold": [asdict(model) for model in running_after_cold],
        "running_models_after_warm": [asdict(model) for model in running_after_warm],
    }
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
    print(f"\nSaved to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
