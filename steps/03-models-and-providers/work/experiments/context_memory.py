"""Step 03, Task 4: a bigger context eats memory (num_ctx, KV cache, offloading).

Run from the work/ folder:  python -m experiments.context_memory
"""
from datetime import datetime
from pathlib import Path
import json

from llm_client import chat, unload_model, LLMError, Role, OLLAMA_MODEL
from model_card import get_json, get_running_models

MACHINE = "personal desktop (i5-14600K, 32 GB DDR5, no dedicated GPU)"
PROMPT = "Say hello in one short sentence."
MAX_TOKENS = 50
CONTEXT_SIZES = [None, 2048, 4096, 8192, 16384, 32768]  # None = don't send num_ctx at all

RESULTS_FILE = Path(__file__).parent / "results" / "context_memory.json"


def measure(context_size: int | None) -> dict:
    messages = [{"role": Role.USER.value, "content": PROMPT}]
    result = chat(messages, temperature=0, max_tokens=MAX_TOKENS, context_size=context_size)

    running = get_running_models()
    # /api/ps always shows the full name with the tag ("qwen2.5:latest"), so OLLAMA_MODEL needs one too.
    model = next((m for m in running if m.name == OLLAMA_MODEL), None)
    if model is None:
        loaded = ", ".join(m.name for m in running) or "nothing"
        raise LLMError(f"{OLLAMA_MODEL} is not in /api/ps (loaded: {loaded}). Use the full name with its tag.")

    return {
        "requested_context": context_size,  # None stays None -> null in the JSON
        "allocated_context": model.context_length,  # what Ollama really reserved (from /api/ps)
        "size_gb": model.size_gb,
        "vram_gb": model.vram_gb,
        "gpu_percent": model.gpu_percent,
        "load_seconds": round(result.load_seconds, 2),
        "tokens_per_second": round(result.output_tokens_per_second, 1),
    }


def print_table(rows: list[dict]) -> None:
    header = f"{'CONTEXT':>10}{'ALLOCATED':>11}{'SIZE GB':>9}{'VRAM GB':>9}{'GPU %':>7}{'LOAD S':>8}{'TOK/S':>7}"
    print(header)
    print("-" * len(header))
    for row in rows:
        # None = we didn't send num_ctx, so Ollama used its default.
        requested = "None" if row["requested_context"] is None else f"{row['requested_context']:,}"
        # Older Ollama versions don't return context_length in /api/ps.
        allocated = "-" if row["allocated_context"] is None else f"{row['allocated_context']:,}"
        print(
            f"{requested:>10}{allocated:>11}{row['size_gb']:>9.2f}{row['vram_gb']:>9.2f}"
            f"{row['gpu_percent']:>7.1f}{row['load_seconds']:>8.2f}{row['tokens_per_second']:>7.1f}"
        )


def main() -> None:
    unload_model()  # start clean, so the None row is a real first load too

    rows = []
    # No unload between sizes on purpose: we want to see what changing num_ctx
    # does to a model that is already loaded.
    for context_size in CONTEXT_SIZES:
        print(f"Measuring context_size={context_size} ...")
        rows.append(measure(context_size))

    print()
    print_table(rows)

    report = {
        "date": datetime.now().isoformat(timespec="seconds"),
        "machine": MACHINE,
        "ollama_version": get_json("/api/version")["version"],
        "model": OLLAMA_MODEL,
        "prompt": PROMPT,
        "max_tokens": MAX_TOKENS,
        "rows": rows,  # requested_context None is saved as null
    }
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
    print(f"\nSaved to {RESULTS_FILE}")


if __name__ == "__main__":
    main()