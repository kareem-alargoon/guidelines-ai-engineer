import os
import httpx
from enum import Enum
from dataclasses import dataclass

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:3b")


class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class LLMError(Exception):
    """Base class for all LLM-related errors."""

@dataclass
class ChatResult:
    text: str
    input_tokens: int
    output_tokens: int
    duration_seconds: float

def convert_from_nanoseconds_to_seconds(nanoseconds: int) -> float:
    return nanoseconds / 1000000000

def chat(messages: list[dict[str, str]], model: str | None = None) -> ChatResult:
    """Send a chat request to the LLM client and return the response."""
    model = model or OLLAMA_MODEL
    url = OLLAMA_URL + "/api/chat"

    for message in messages:
        if message["role"] not in Role:
            raise LLMError(f"Invalid role: {message['role']}")

    try:
        response = httpx.post(
            url,
            json={"model": model, "messages": messages, "stream": False},
            timeout=120,
        )

    except httpx.ConnectError as e:
        raise LLMError(f"Error sending chat request: Please check your network connection and ensure that the Ollama server is running.")

    if response.status_code == 404:
        raise LLMError(f"Model not found: {model}, Please check your model name and ensure that the model is installed.")

    response.raise_for_status()
    data = response.json()
    return ChatResult(
        text=data["message"]["content"],
        input_tokens=data.get("prompt_eval_count", 0),
        output_tokens=data["eval_count"],
        duration_seconds=convert_from_nanoseconds_to_seconds(data["total_duration"]),
    )



if __name__ == "__main__":
    chat_result = chat([{"role": "user", "content": "ما هى عاصمة مصر"}])
    print(chat_result.text)
    print(f"in: {chat_result.input_tokens} | out: {chat_result.output_tokens} | {chat_result.duration_seconds}")