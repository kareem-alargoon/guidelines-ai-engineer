from datetime import datetime
from pathlib import Path
import json
from llm_client import chat, Role

questions = [
    "Who is the author of the book 'The Great Gatsby'?",
    "What is the capital of France?",
    "Who is the president of the United States?",

    "What is the story of the novel 'The Dark Night' by 'Naguib Mahfouz'?",
    "In what year did 'Adel Imam' receive the 'Nobel Prize'?",
    "اين كتب احمد شوقى قصيدة 'الرجل والبنت'؟"
]

results = []
for question in questions:
    for attempt in range(1, 4):
        print("Q (attempt " + str(attempt) + "): " + question)
        result = chat([{"role": Role.USER.value, "content": question}])
        print("A: " + result.text)
        print(f"in: {result.input_tokens} tokens | out: {result.output_tokens} tokens | {result.duration_seconds:.2f} s")
        results.append({"attempt": attempt, "question": question, "result": result.text,
                        "in_tokens": result.input_tokens, "out_tokens": result.output_tokens,
                        "duration_seconds": result.duration_seconds, "time": datetime.now().isoformat()})

here = Path(__file__).parent
folder = here / "results"
folder.mkdir(parents=True, exist_ok=True)

file_path = folder / "hallucination.json"
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)


