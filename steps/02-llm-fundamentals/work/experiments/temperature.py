from datetime import datetime
from pathlib import Path
import json
from llm_client import chat, Role, LLMError

PROMPTS = [
    {
        "kind": "single_answer",
        "text": "ما هي عاصمة اليابان؟ جاوب بكلمة واحدة فقط.",
    },
    {
        "kind": "creative",
        "text": "اقترح اسم واحد بس لمحل قهوة في المعادي. اكتب الاسم بس من غير أي شرح.",
    },
    {
        "kind": "classification",
        "text": (
            "صنّف رسالة العميل دي لواحدة من التلاتة: شكوى، استفسار، شكر.\n"
            "رد بكلمة واحدة بس من التلاتة دول.\n\n"
            "الرسالة: \"الأوردر وصل متأخر يومين والعلبة كانت مفتوحة.\""
        ),
    },
]

TEMPERATURES = [0, 0.7, 1.5]
ATTEMPTS = 5

here = Path(__file__).parent
folder = here / "results"
folder.mkdir(parents=True, exist_ok=True)
file_path = folder / "temperature.json"


def save(results: list[dict]) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


def count_distinct(responses: list[str]) -> int:
    """Count how many different responses there are, ignoring leading/trailing whitespace."""
    return len({response.strip() for response in responses})


def print_summary(results: list[dict]) -> None:
    """Print a (prompt kind x temperature) table of distinct responses, e.g. 4/5."""
    print()
    print("Distinct responses per (prompt, temperature):")
    print(f"{'kind':<16}" + "".join(f"{'T=' + str(t):>8}" for t in TEMPERATURES))
    for prompt in PROMPTS:
        row = f"{prompt['kind']:<16}"
        for temperature in TEMPERATURES:
            responses = [
                r["response"]
                for r in results
                if r["kind"] == prompt["kind"] and r["temperature"] == temperature and r["seed"] is None
            ]
            row += f"{f'{count_distinct(responses)}/{len(responses)}':>8}"
        print(row)


def ask(prompt: dict, temperature: float, attempt: int, seed: int | None = None) -> dict | None:
    """Send one prompt and return a result row, or None if the request failed."""
    print(f"[{prompt['kind']} | T={temperature} | seed={seed} | attempt {attempt}]")
    try:
        result = chat(
            [{"role": Role.USER.value, "content": prompt["text"]}],
            temperature=temperature,
            seed=seed,
        )
    except LLMError as e:
        print(f"Skipped: {e}")
        return None
    print(f"A: {result.text}")
    return {
        "kind": prompt["kind"],
        "prompt": prompt["text"],
        "temperature": temperature,
        "seed": seed,
        "attempt": attempt,
        "response": result.text,
        "in_tokens": result.input_tokens,
        "out_tokens": result.output_tokens,
        "duration_seconds": result.duration_seconds,
        "stop_reason": result.stop_reason,
        "run_at": run_at,
    }


def print_seed_summary(results: list[dict]) -> None:
    """For each seed, print its responses and whether they are all identical."""
    print()
    print(f"Seed experiment (creative prompt, T={SEED_TEMPERATURE}):")
    for seed in SEEDS:
        responses = [r["response"].strip() for r in results if r["seed"] == seed]
        verdict = "identical" if count_distinct(responses) == 1 else "DIFFERENT"
        print(f"seed={seed}: {verdict} -> {responses}")


SEED_TEMPERATURE = 1.0
SEEDS = [42, 7]
SEED_REPEATS = 2

run_at = datetime.now().isoformat()
results = []

# Part 1: every prompt, ATTEMPTS times on every temperature (no seed)
for prompt in PROMPTS:
    for temperature in TEMPERATURES:
        for attempt in range(1, ATTEMPTS + 1):
            row = ask(prompt, temperature, attempt)
            if row:
                results.append(row)
                save(results)

# Part 2: the creative prompt, same temperature, each seed SEED_REPEATS times
creative = next(p for p in PROMPTS if p["kind"] == "creative")
for seed in SEEDS:
    for attempt in range(1, SEED_REPEATS + 1):
        row = ask(creative, SEED_TEMPERATURE, attempt, seed=seed)
        if row:
            results.append(row)
            save(results)

print_summary(results)
print_seed_summary(results)
print(f"Saved {len(results)} answers to {file_path}")