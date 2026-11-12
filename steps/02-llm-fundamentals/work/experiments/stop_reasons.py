from datetime import datetime
from pathlib import Path
import json
from llm_client import chat, Role, LLMError, ChatResult


CITIES_PROMPT = "اكتب لستة JSON فيها أسماء 10 مدن مصرية. رد بالـ JSON بس من غير أي كلام تاني."
COUNT_PROMPT = "عدّ من 1 لـ 20، كل رقم في سطر لوحده. اكتب الأرقام بس."

SHORT_MAX_TOKENS = 15

STOP_WORDS = ["7"]

TRUNCATED_REASONS = {"length", "max_tokens"}


here = Path(__file__).parent
folder = here / "results"
folder.mkdir(parents=True, exist_ok=True)
file_path = folder / "stop_reasons.json"

def save(results: list[dict]) -> None:
    """Write all result rows to stop_reasons.json, keeping Arabic readable."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


class TruncatedResponseError(LLMError):
    """The model was cut off (hit max_tokens), so the response is incomplete."""


class InvalidJSONError(LLMError):
    """The model finished normally, but its response is not valid JSON."""


def ask(experiment: str, prompt: str, *, max_tokens: int | None = None, stop: list[str] | None = None, parse_json: bool = False) -> dict | None:
    """Send one prompt and return a result row, or None if the request failed."""
    print(f"\n[{experiment} | max_tokens={max_tokens} | stop={stop}]")
    try:
        result = chat(
            [{"role": Role.USER.value, "content": prompt}],
            max_tokens=max_tokens,
            stop=stop
        )
    except LLMError as e:
        print(f"Skipped: {e}")
        return None
    print(f"A: {result.text}")
    print(f"S: {result.stop_reason}")
    print(f"O: {result.output_tokens}")
    parse = try_parse(result) if parse_json else None
    print(f"P: {parse}")
    return {
        "experiment": experiment,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "stop": stop,
        "parse": parse,
        "response": result.text,
        "in_tokens": result.input_tokens,
        "out_tokens": result.output_tokens,
        "duration_seconds": result.duration_seconds,
        "stop_reason": result.stop_reason,
        "run_at": run_at,
    }


def parse_json_result(result: ChatResult) -> dict | list:
    """Parse the model's response as JSON, checking the stop reason first.

    Raises TruncatedResponseError if the response was cut off, and
    InvalidJSONError (with the first 200 characters) if it isn't valid JSON.
    """
    if result.stop_reason in TRUNCATED_REASONS:
        raise TruncatedResponseError(f"Truncated response for stop_reason: {result.stop_reason}")

    try:
        return json.loads(result.text)
    except json.decoder.JSONDecodeError as e:
        raise InvalidJSONError(f"Invalid JSON, the text is {result.text[:200]}") from e


def try_parse(result: ChatResult) -> str:
    """Try parse_json_result and return a short status line instead of raising."""
    try:
        parsed = parse_json_result(result)
        return f"ok: {len(parsed)} items"
    except (TruncatedResponseError, InvalidJSONError) as e:
        return f"{type(e).__name__}: {e}"


run_at = datetime.now().isoformat()
results = []

row = ask("cities", CITIES_PROMPT, max_tokens=SHORT_MAX_TOKENS, parse_json=True)
if row:
    results.append(row)
row = ask("cities", CITIES_PROMPT, parse_json=True)
if row:
    results.append(row)
row = ask("count", COUNT_PROMPT, stop=STOP_WORDS)
if row:
    results.append(row)

save(results)
print(f"Saved {len(results)} answers to {file_path}")