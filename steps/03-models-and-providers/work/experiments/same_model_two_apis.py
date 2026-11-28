"""Step 03, Task 5: same model, same server, two APIs. Do the answers match?

Native /api/chat (OllamaProvider) vs OpenAI-compatible /v1/chat/completions (OpenAICompatibleProvider),
both on qwen2.5:3b with the default context, temperature=0 and seed=42.
For each prompt: native, then openai_compat, then native again (the control: if native vs native
also differs, the difference doesn't come from the API).

Run from the work/ folder:  python -m experiments.same_model_two_apis
"""
from datetime import datetime
from pathlib import Path
import json

from llm_client import OLLAMA_URL, Role
from model_card import get_json
from providers import LLMProvider, OllamaProvider, OpenAICompatibleProvider

MACHINE = "personal desktop (i5-14600K, 32 GB DDR5, no dedicated GPU)"
# Same model name and same (default) context in both, so switching APIs never reloads the model.
MODEL = "qwen2.5:3b"
BASE_URL = OLLAMA_URL + "/v1"
SETTINGS = {"temperature": 0, "seed": 42, "max_tokens": 200}
PROMPTS = [
    "Explain what an API is in two sentences.",
    "اشرح يعني إيه cache في جملتين.",
    "Write a Python function that checks if a number is prime.",
    "What is the capital of Australia? Answer in one word.",
    "List 5 fruits, one per line, no extra text.",
]

RESULTS_FILE = Path(__file__).parent / "results" / "same_model_two_apis.json"


def run_once(provider: LLMProvider, prompt: str) -> dict:
    result = provider.chat([{"role": Role.USER.value, "content": prompt}], **SETTINGS)
    return {
        "text": result.text,
        "input_tokens": result.input_tokens,
        "output_tokens": result.output_tokens,
        "duration_seconds": round(result.duration_seconds, 2),
        "stop_reason": result.stop_reason,
    }


def print_table(rows: list[dict]) -> None:
    print(f"\n{'prompt':<32} {'compat=native':>13} {'native2=native':>14} "
          f"{'in n/c':>8} {'out n/c/n2':>11} {'time n/c (s)':>13}")
    for row in rows:
        n, c, n2 = row["native"], row["openai_compat"], row["native_again"]
        print(
            f"{row['prompt'][:30]:<32} {str(row['compat_same_as_native']):>13} "
            f"{str(row['native_again_same_as_native']):>14} "
            f"{n['input_tokens']:>3}/{c['input_tokens']:<4} "
            f"{n['output_tokens']:>3}/{c['output_tokens']}/{n2['output_tokens']:<3} "
            f"{n['duration_seconds']:>6.2f}/{c['duration_seconds']:<6.2f}"
        )


def main() -> None:
    native = OllamaProvider(MODEL)
    compat = OpenAICompatibleProvider(BASE_URL, "ollama", MODEL)

    # Warm-up: load the model once so the first prompt isn't a cold start.
    for provider in (native, compat):
        provider.chat([{"role": Role.USER.value, "content": "Hi"}], **SETTINGS)

    rows = []
    for prompt in PROMPTS:
        print(f"Running: {prompt[:40]}")
        first = run_once(native, prompt)
        second = run_once(compat, prompt)
        third = run_once(native, prompt)
        rows.append({
            "prompt": prompt,
            "compat_same_as_native": second["text"] == first["text"],
            "native_again_same_as_native": third["text"] == first["text"],
            "native": first,
            "openai_compat": second,
            "native_again": third,
        })

    print_table(rows)

    report = {
        "date": datetime.now().isoformat(timespec="seconds"),
        "machine": MACHINE,
        "ollama_version": get_json("/api/version")["version"],
        "model": MODEL,
        "settings": SETTINGS,
        "order": "native, openai_compat, native_again for each prompt",
        "results": rows,
    }
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
    print(f"\nSaved to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
