import json
import os
import httpx
from typing import Any

from enum import Enum
from dataclasses import dataclass

# 127.0.0.1, not "localhost": on Windows "localhost" tries IPv6 (::1) first, Ollama only
# listens on IPv4, and every request lost ~2 s before falling back (measured in Step 03, Task 3).
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
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
    stop_reason: str
    # Where the time went (Step 03, Task 3). Defaults keep old ChatResult(...) calls working.
    load_seconds: float = 0.0  # loading the model from disk into memory (cold start)
    prompt_eval_seconds: float = 0.0  # reading the prompt (prefill)
    eval_seconds: float = 0.0  # generating the answer token by token (decode)

    @property
    def output_tokens_per_second(self) -> float:
        # Generation speed only: divide by eval time, not total time,
        # otherwise a cold start (load) makes the model look slow.
        if self.eval_seconds <= 0:
            return 0.0
        return self.output_tokens / self.eval_seconds


def convert_from_nanoseconds_to_seconds(nanoseconds: int) -> float:
    return nanoseconds / 1e9


def send_request(url: str, body: dict[str, Any], timeout: float) -> httpx.Response:
    try:
        return httpx.post(url, json=body, timeout=timeout)
    except httpx.ConnectError as e:
        raise LLMError(f"Can't reach Ollama at {OLLAMA_URL}. Make sure the Ollama app is running.") from e
    except httpx.TimeoutException as e:
        raise LLMError(
            f"Ollama didn't answer within {timeout}s. "
            "The model may still be loading."
        ) from e


def handle_http_errors(response: httpx.Response, model: str) -> None:
    if response.status_code == 404:
        raise LLMError(f"Model not found: {model}. Download it with: ollama pull {model}")

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise LLMError(f"Ollama returned HTTP {response.status_code}: {response.text}") from e


def validate_params(temperature: float | None, top_p: float | None) -> None:
    if temperature is not None and temperature < 0:
        raise LLMError(f"Temperature must be greater than or equal to zero: {temperature}")
    if top_p is not None and not 0 <= top_p <= 1:
        raise LLMError(f"Top p must be between 0 and 1, not {top_p}")


def get_options(
        *,
        temperature: float | None = None,
        top_k: int | None = None,
        top_p: float | None = None,
        seed: int | None = None,
        max_tokens: int | None = None,
        stop: list[str] | None = None,
        context_size: int | None = None
) -> dict | None:
    options = {
        key: value
        for key, value in {
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
            "seed": seed,
            "num_predict": max_tokens,
            "stop": stop,
            "num_ctx": context_size
        }.items()
        if value is not None
    }

    return options or None


def chat(
        messages: list[dict[str, str]],
        model: str | None = None,
        *,
        temperature: float | None = None,
        top_k: int | None = None,
        top_p: float | None = None,
        seed: int | None = None,
        max_tokens: int | None = None,
        stop: list[str] | None = None,
        format: dict[str, Any] | str | None = None,
        context_size: int | None = None,
        keep_alive: str | int | None = None
) -> ChatResult:
    """Send a chat request to Ollama and return a ChatResult.

    Raises LLMError for every expected failure (Ollama not running, timeout,
    model not found, any other HTTP error), so callers only need to catch one type.
    """
    model = model or OLLAMA_MODEL
    url = OLLAMA_URL + "/api/chat"

    validate_params(temperature, top_p)

    for message in messages:
        role = message.get("role")
        if role not in VALID_ROLES:
            raise LLMError(f"Invalid role: {role!r}. Use one of: {', '.join(sorted(VALID_ROLES))}")

    options = get_options(temperature=temperature, top_k=top_k, top_p=top_p, seed=seed, max_tokens=max_tokens,
                          stop=stop, context_size=context_size)

    body = {"model": model, "messages": messages, "stream": False}

    if options:
        body["options"] = options

    if format:
        body["format"] = format

    # keep_alive goes in the body itself, not in options. "10m", 3600, -1 (forever), 0 (unload now).
    # Check `is not None`, not truthiness: keep_alive=0 is falsy but must still be sent.
    if keep_alive is not None:
        body["keep_alive"] = keep_alive

    response = send_request(url, body, TIMEOUT_SECONDS)
    handle_http_errors(response, model)

    data = response.json()
    return ChatResult(
        text=data["message"]["content"],
        input_tokens=data.get("prompt_eval_count", 0),
        output_tokens=data.get("eval_count", 0),
        duration_seconds=convert_from_nanoseconds_to_seconds(data.get("total_duration", 0)),
        stop_reason=data.get("done_reason", "Unknown"),
        load_seconds=convert_from_nanoseconds_to_seconds(data.get("load_duration", 0)),
        prompt_eval_seconds=convert_from_nanoseconds_to_seconds(data.get("prompt_eval_duration", 0)),
        eval_seconds=convert_from_nanoseconds_to_seconds(data.get("eval_duration", 0)),
    )


if __name__ == "__main__":
    chat_result = chat([{"role": Role.USER.value, "content": "اشرحلى اكثر تاريخ اثارة فى القاهرة فى 5 فقرات"}],
                       temperature=0, max_tokens=20)
    print(chat_result.text)
    print(
        f"in: {chat_result.input_tokens} tokens | out: {chat_result.output_tokens} tokens | {chat_result.duration_seconds:.2f} s | stop_reason: {chat_result.stop_reason}")
    print(
        f"load: {chat_result.load_seconds:.2f} s | prompt eval: {chat_result.prompt_eval_seconds:.2f} s | "
        f"eval: {chat_result.eval_seconds:.2f} s | {chat_result.output_tokens_per_second:.1f} tokens/s")
