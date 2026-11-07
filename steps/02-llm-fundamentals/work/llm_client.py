import os
import httpx
from enum import Enum
from dataclasses import dataclass

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434").rstrip("/")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:3b")
TIMEOUT_SECONDS = 120


class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


VALID_ROLES = {role.value for role in Role}


class LLMError(Exception):
    """Base class for all LLM-related errors."""


@dataclass
class ChatResult:
    text: str
    input_tokens: int
    output_tokens: int
    duration_seconds: float


def convert_from_nanoseconds_to_seconds(nanoseconds: int) -> float:
    return nanoseconds / 1e9


def chat(messages: list[dict[str, str]], model: str | None = None) -> ChatResult:
    """Send a chat request to Ollama and return a ChatResult.

    Raises LLMError for every expected failure (Ollama not running, timeout,
    model not found, any other HTTP error), so callers only need to catch one type.
    """
    model = model or OLLAMA_MODEL
    url = OLLAMA_URL + "/api/chat"

    for message in messages:
        role = message.get("role")
        if role not in VALID_ROLES:
            raise LLMError(f"Invalid role: {role!r}. Use one of: {', '.join(sorted(VALID_ROLES))}")

    try:
        response = httpx.post(
            url,
            json={"model": model, "messages": messages, "stream": False},
            timeout=TIMEOUT_SECONDS,
        )
    except httpx.ConnectError as e:
        raise LLMError(f"Can't reach Ollama at {OLLAMA_URL}. Make sure the Ollama app is running.") from e
    except httpx.TimeoutException as e:
        raise LLMError(
            f"Ollama didn't answer within {TIMEOUT_SECONDS}s. "
            "The model may still be loading, or the answer is too long. Try again or ask for a shorter answer."
        ) from e

    if response.status_code == 404:
        raise LLMError(f"Model not found: {model}. Download it with: ollama pull {model}")

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise LLMError(f"Ollama returned HTTP {response.status_code}: {response.text}") from e

    data = response.json()
    return ChatResult(
        text=data["message"]["content"],
        input_tokens=data.get("prompt_eval_count", 0),
        output_tokens=data.get("eval_count", 0),
        duration_seconds=convert_from_nanoseconds_to_seconds(data.get("total_duration", 0)),
    )


if __name__ == "__main__":
    chat_result = chat([{"role": Role.USER.value, "content": "اشرحلى اكثر تاريخ اثارة فى القاهرة فى 5 فقرات"}])
    print(chat_result.text)
    print(f"in: {chat_result.input_tokens} tokens | out: {chat_result.output_tokens} tokens | {chat_result.duration_seconds:.2f} s")
