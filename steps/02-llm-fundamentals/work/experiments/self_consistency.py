from datetime import datetime
from pathlib import Path
import json
import time
from llm_client import chat, Role, LLMError, OLLAMA_MODEL, ChatResult
from pydantic import BaseModel, ValidationError
from collections import Counter
from collections.abc import Callable


class DirectAnswer(BaseModel):
    answer: int

class ReasonedAnswer(BaseModel):
    reasoning: str
    answer: int


# ---------- Step 2: solve_direct ----------

DIRECT_PROMPT = """Solve the math word problem the user sends.
Reply with JSON only: {"answer": integer}
The answer is the final number only, without units."""

DIRECT_SCHEMA = DirectAnswer.model_json_schema()  # generated from the pydantic model


def solve_direct(problem: str, temperature: float) -> tuple[int | None, ChatResult]:
    """Ask for the final number right away, with no reasoning.

    Returns (answer, result). answer is None when the reply does not match the schema.
    LLMError is not caught here: the caller decides what to do with it.
    """
    messages = [
        {"role": Role.SYSTEM.value, "content": DIRECT_PROMPT},
        {"role": Role.USER.value, "content": problem},
    ]
    result = chat(messages, temperature=temperature, format=DIRECT_SCHEMA)

    try:
        parsed = DirectAnswer.model_validate_json(result.text)
    except ValidationError:
        return None, result

    return parsed.answer, result


# ---------- Step 3: solve_with_reasoning ----------

# The schema alone only says a "reasoning" field must exist, not what goes in it.
# This prompt asks for the actual working, so the model writes the steps before the number.
REASONING_PROMPT = """Solve the math word problem the user sends.
First write your step-by-step working in "reasoning", then put the final number in "answer".
Reply with JSON only: {"reasoning": string, "answer": integer}
The answer is the final number only, without units."""

REASONING_SCHEMA = ReasonedAnswer.model_json_schema()  # "reasoning" comes before "answer"


def solve_with_reasoning(problem: str, temperature: float) -> tuple[int | None, ChatResult]:
    """Same as solve_direct, but the model writes its working before the final number.

    The schema puts "reasoning" before "answer", so when the model writes the answer
    tokens, its working is already in the context (Karpathy: models need tokens to think).
    Returns (answer, result). answer is None when the reply does not match the schema.
    """
    messages = [
        {"role": Role.SYSTEM.value, "content": REASONING_PROMPT},
        {"role": Role.USER.value, "content": problem},
    ]
    result = chat(messages, temperature=temperature, format=REASONING_SCHEMA)

    try:
        parsed = ReasonedAnswer.model_validate_json(result.text)
    except ValidationError:
        return None, result

    return parsed.answer, result


# ---------- Step 4: majority_vote ----------

def majority_vote(answers: list[int | None]) -> int | None:
    """Return the answer that appears most often, ignoring None (failed replies).

    Returns None when there is no valid answer at all.
    Tie: returns the tied answer that appeared first in the list. Counter.most_common
    keeps first-seen order for equal counts, so the result is always the same for the
    same input. Returning None on a tie would also be valid ("the model is not sure"),
    but then a 2-2 tie counts as wrong even when one of the two answers is correct.
    """
    valid = [answer for answer in answers if answer is not None]
    if not valid:
        return None

    counts = Counter(valid)
    most_common_answer, _count = counts.most_common(1)[0]
    return most_common_answer


# ---------- Step 5: run_setting ----------

# The type of solve_direct and solve_with_reasoning:
# takes (problem, temperature) and returns (answer, ChatResult).
Solver = Callable[[str, float], tuple[int | None, ChatResult]]


def run_setting(problems: list[dict], solve: Solver, runs: int, temperature: float) -> list[dict]:
    """Run one setting on every problem: `runs` tries each, then majority vote.

    Returns one row per problem. output_tokens is the total of all tries for that
    problem, because with self-consistency you pay for every try, not only the winner.
    A try that fails with LLMError counts as None (no answer) and is counted in llm_errors.
    """
    rows = []
    for problem in problems:
        answers = []
        output_tokens = 0
        llm_errors = 0

        for run in range(1, runs + 1):
            print(f"  problem {problem['id']} | try {run}/{runs}")
            try:
                answer, result = solve(problem["problem"], temperature)
            except LLMError as e:
                print(f"    LLMError: {e}")
                answers.append(None)
                llm_errors += 1
                continue
            answers.append(answer)
            output_tokens += result.output_tokens

        final = majority_vote(answers)
        rows.append({
            "id": problem["id"],
            "difficulty": problem["difficulty"],
            "answers": answers,
            "final_answer": final,
            "correct_answer": problem["answer"],
            "is_correct": final == problem["answer"],
            "output_tokens": output_tokens,
            "llm_errors": llm_errors,
        })
    return rows


# ---------- Quick tests ----------

# majority_vote: no Ollama needed.
assert majority_vote([5, 5, 3, None, 5]) == 5
assert majority_vote([None, None, None]) is None
assert majority_vote([]) is None
assert majority_vote([7]) == 7
assert majority_vote([5, 5, 3, 3, None]) == 5  # tie: 5 appeared first
assert majority_vote([3, 3, 5, 5, None]) == 3  # tie: 3 appeared first
assert majority_vote([None, None, 4]) == 4     # None never wins, even if it's the most common
print("majority_vote: all tests passed")


work_folder = Path(__file__).parent.parent
with open(work_folder / "data" / "math_problems.json", encoding="utf-8") as f:
    problems = json.load(f)["problems"]

# solve_direct / solve_with_reasoning: needs Ollama. Commented out so the run is fast.
# for p in [problems[0], problems[-1]]:
#     for name, solve in [("direct", solve_direct), ("reasoning", solve_with_reasoning)]:
#         answer, result = solve(p["problem"], temperature=0)
#         print(f"problem {p['id']} | {name:<9} | model = {answer} | correct = {p['answer']} "
#               f"| output tokens = {result.output_tokens}")



# ---------- Step 6: the 4 settings, the table, and the JSON file ----------

# Settings 1-2: one try at T=0, the model's single "best guess".
# Settings 3-4: 5 tries at T=0.8, so the tries differ and voting has something to choose from.
# (At T=0 the 5 tries would be the same answer 5 times, as we saw in Task 3.)
SETTINGS = [
    {"name": "direct x1 T=0",      "solve": solve_direct,         "runs": 1, "temperature": 0},
    {"name": "reasoning x1 T=0",   "solve": solve_with_reasoning, "runs": 1, "temperature": 0},
    {"name": "direct x5 T=0.8",    "solve": solve_direct,         "runs": 5, "temperature": 0.8},
    {"name": "reasoning x5 T=0.8", "solve": solve_with_reasoning, "runs": 5, "temperature": 0.8},
]


def run_all_settings(problems: list[dict]) -> list[dict]:
    """Run every setting and return one result per setting, with its rows and its totals."""
    results = []
    for setting in SETTINGS:
        print(f"\n=== {setting['name']} ===")
        started = time.perf_counter()
        rows = run_setting(problems, setting["solve"], setting["runs"], setting["temperature"])
        seconds = time.perf_counter() - started

        correct = sum(row["is_correct"] for row in rows)
        total_tokens = sum(row["output_tokens"] for row in rows)
        results.append({
            "name": setting["name"],
            "solver": setting["solve"].__name__,  # the function itself can't be saved in JSON, its name can
            "runs": setting["runs"],
            "temperature": setting["temperature"],
            "correct": correct,
            "total": len(rows),
            "avg_output_tokens_per_problem": round(total_tokens / len(rows), 1),
            "llm_errors": sum(row["llm_errors"] for row in rows),
            "seconds": round(seconds, 1),
            "rows": rows,
        })
    return results


def print_table(results: list[dict]) -> None:
    print(f"\n{'setting':<20} {'correct':>8} {'avg out tokens':>15} {'errors':>7} {'seconds':>8}")
    for r in results:
        score = f"{r['correct']}/{r['total']}"
        print(f"{r['name']:<20} {score:>8} {r['avg_output_tokens_per_problem']:>15} "
              f"{r['llm_errors']:>7} {r['seconds']:>8}")


def save(results: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "run_at": datetime.now().isoformat(),
        "model": OLLAMA_MODEL,
        "settings": results,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)


results = run_all_settings(problems)
results_path = Path(__file__).parent / "results" / "self_consistency.json"
save(results, results_path)
print_table(results)
print(f"\nSaved to {results_path}")
