from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json
import re
import time
from llm_client import chat, Role, LLMError, OLLAMA_MODEL
from pydantic import BaseModel, ValidationError

class OrderItem(BaseModel):
    product: str
    quantity: int

class Order(BaseModel):
    customer_name: str | None
    items: list[OrderItem]
    city: str | None
    is_urgent: bool

# 0.7, not 0: at T=0 the 3 runs give the same answer (Task 3), so they add no information.
# At 0.7 we measure how stable each method is when there is real randomness.
TEMPERATURE = 0.7
RUNS = 3

EXTRACTION_PROMPT = """You extract order data from a customer message sent to an online shop.

Return a JSON object with exactly these keys:
{
  "customer_name": string or null,
  "items": [{"product": string, "quantity": integer}],
  "city": string or null,
  "is_urgent": boolean
}

Rules:
- customer_name and city: use null if the message does not mention them. Never guess.
- quantity: an integer. If no number is given for a product, use 1.
- is_urgent: true only if the customer asks for fast delivery or gives a deadline.
- Write product, customer_name and city in the same language the message uses.

Reply with the JSON object only."""


def build_messages(message: str) -> list[dict[str, str]]:
    """The same system prompt + customer message, shared by all three methods."""
    return [
        {"role": Role.SYSTEM.value, "content": EXTRACTION_PROMPT},
        {"role": Role.USER.value, "content": message},
    ]


def extract_prompt_only(message: str) -> str:
    """Method 1: ask for JSON in the prompt and return the raw text, no cleanup."""
    result = chat(build_messages(message), temperature=TEMPERATURE)
    return result.text


# Seen in method 1 (message 7, at T=0 and T=0.7): {"product": "...", 2}
# The "quantity" key is missing before the number.
MISSING_QUANTITY_KEY = re.compile(r'("product"\s*:\s*"[^"]*")\s*,\s*(\d+)\s*}')


def clean_json_text(text: str) -> str:
    """Fix the format mistakes the model is known to make, before json.loads."""
    # Defensive, not seen in our results: keep only what is between the first { and the last }.
    # This removes markdown code fences and any text around the JSON.
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        text = text[start:end + 1]

    # Seen in our results: put back the missing "quantity" key.
    text = MISSING_QUANTITY_KEY.sub(r'\1, "quantity": \2}', text)

    return text


def extract_with_cleanup(message: str) -> str:
    """Method 2: same prompt as method 1, then fix known format mistakes."""
    return clean_json_text(extract_prompt_only(message))


ORDER_SCHEMA = Order.model_json_schema()  # generated from the pydantic model, not written by hand


def extract_with_schema(message: str) -> str:
    """Method 3: same prompt, plus the JSON schema in Ollama's format (constrained sampling)."""
    result = chat(build_messages(message), temperature=TEMPERATURE, format=ORDER_SCHEMA)
    return result.text


METHODS = {
    "prompt_only": extract_prompt_only,
    "cleanup": extract_with_cleanup,
    "schema": extract_with_schema,
}


# ---------- Step 7: (a) valid JSON? (b) matches the schema? ----------

@dataclass
class Check:
    valid_json: bool
    matches_schema: bool
    order: Order | None
    error: str | None


def validate(text: str) -> Check:
    """Two separate steps, so we know which one failed."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        return Check(False, False, None, f"JSONDecodeError: {e}")

    try:
        order = Order.model_validate(data)
    except ValidationError as e:
        return Check(True, False, None, f"ValidationError: {e.error_count()} errors")

    return Check(True, True, order, None)


# ---------- Step 8: (c) is the data correct? ----------
# quantity, is_urgent and null vs not null: exact.
# product, customer_name and city: compared after normalize(), so spelling variants
# like "اسكندرية" / "الإسكندرية" or "لاب توب" / "لابتوب" count as the same.
# A different word ("بنطال" vs "بنطلون") is still wrong.

def normalize(text: str | None) -> str | None:
    if text is None:
        return None
    text = text.strip().lower()
    text = re.sub("[أإآ]", "ا", text)
    text = text.replace("ة", "ه").replace("ى", "ي")
    words = [word.removeprefix("ال") for word in text.split()]
    return "".join(words)


def wrong_fields(order: Order, expected: dict) -> list[str]:
    """Return the names of the fields that don't match the answer key. Empty list = correct."""
    wrong = []
    if normalize(order.customer_name) != normalize(expected["customer_name"]):
        wrong.append("customer_name")
    if normalize(order.city) != normalize(expected["city"]):
        wrong.append("city")
    if order.is_urgent != expected["is_urgent"]:
        wrong.append("is_urgent")

    # sorted, so the order of items does not matter; a duplicated item makes the lists differ
    got = sorted((normalize(item.product), item.quantity) for item in order.items)
    want = sorted((normalize(item["product"]), item["quantity"]) for item in expected["items"])
    if got != want:
        wrong.append("items")
    return wrong


# ---------- Step 10: run everything and save ----------

def run_all(orders: list[dict]) -> list[dict]:
    rows = []
    total = len(orders) * len(METHODS) * RUNS
    count = 0
    for order in orders:
        for method_name, extract in METHODS.items():
            for run in range(1, RUNS + 1):
                count += 1
                print(f"[{count}/{total}] order {order['id']} | {method_name} | run {run}")
                row = {"order_id": order["id"], "method": method_name, "run": run}

                started = time.perf_counter()
                try:
                    text = extract(order["message"])
                except LLMError as e:
                    print(f"  Skipped: {e}")
                    rows.append(row | {"llm_error": str(e)})
                    continue
                row["duration_seconds"] = round(time.perf_counter() - started, 2)

                check = validate(text)
                wrong = wrong_fields(check.order, order["expected"]) if check.order else None
                rows.append(row | {
                    "llm_error": None,
                    "response": text,
                    "valid_json": check.valid_json,
                    "matches_schema": check.matches_schema,
                    "correct": wrong == [],
                    "wrong_fields": wrong,
                    "error": check.error,
                })
    return rows


def save(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "run_at": datetime.now().isoformat(),
        "model": OLLAMA_MODEL,
        "temperature": TEMPERATURE,
        "runs_per_message": RUNS,
        "rows": rows,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)


# ---------- Step 11: the table ----------

def print_table(rows: list[dict]) -> None:
    print(f"\n{'method':<12} {'n':>3} {'(a) JSON':>9} {'(b) schema':>11} {'(c) correct':>12} {'avg s':>6}")
    for method_name in METHODS:
        done = [r for r in rows if r["method"] == method_name and r["llm_error"] is None]
        n = len(done)
        if n == 0:
            print(f"{method_name:<12} no successful requests")
            continue
        a = sum(r["valid_json"] for r in done) / n
        b = sum(r["matches_schema"] for r in done) / n
        c = sum(r["correct"] for r in done) / n
        avg = sum(r["duration_seconds"] for r in done) / n
        print(f"{method_name:<12} {n:>3} {a:>9.0%} {b:>11.0%} {c:>12.0%} {avg:>6.2f}")


work_folder = Path(__file__).parent.parent
with open(work_folder / "data" / "orders.json", encoding="utf-8") as f:
    orders = json.load(f)["orders"]

results_path = Path(__file__).parent / "results" / "structured.json"
rows = run_all(orders)
save(rows, results_path)
print_table(rows)
print(f"\nSaved {len(rows)} rows to {results_path}")

