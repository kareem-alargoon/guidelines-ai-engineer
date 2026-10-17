from datetime import datetime
from pathlib import Path
import json
from llm_client import chat, Role, LLMError

questions = [
    "Who is the author of the book 'The Great Gatsby'?",
    "What is the capital of France?",
    "Who is the president of the United States?",

    "What is the story of the novel 'The Dark Night' by 'Naguib Mahfouz'?",
    "In what year did 'Adel Imam' receive the 'Nobel Prize'?",
    "اين كتب احمد شوقى قصيدة 'الرجل والبنت'؟"
]

ATTEMPTS = 3

here = Path(__file__).parent
folder = here / "results"
folder.mkdir(parents=True, exist_ok=True)
file_path = folder / "hallucination.json"


def save(results: list[dict]) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


run_at = datetime.now().isoformat()
results = []
for question in questions:
    for attempt in range(1, ATTEMPTS + 1):
        print(f"Q (attempt {attempt}): {question}")
        try:
            result = chat([{"role": Role.USER.value, "content": question}])
        except LLMError as e:
            print(f"Skipped: {e}")
            continue
        print(f"A: {result.text}")
        print(f"in: {result.input_tokens} tokens | out: {result.output_tokens} tokens | {result.duration_seconds:.2f} s")
        results.append({
            "attempt": attempt,
            "question": question,
            "response": result.text,
            "in_tokens": result.input_tokens,
            "out_tokens": result.output_tokens,
            "duration_seconds": result.duration_seconds,
            "run_at": run_at,
        })
        save(results)  # save after every answer, so a failure later doesn't lose what we already have

print(f"Saved {len(results)} answers to {file_path}")
