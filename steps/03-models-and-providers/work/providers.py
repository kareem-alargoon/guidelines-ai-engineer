"""LLM providers behind one interface, like Laravel drivers (Step 03, Task 5).

App code calls provider.chat(...) and doesn't care who answers.
The provider is picked from environment variables, like MAIL_MAILER or DB_CONNECTION.
"""
import os
import time
from abc import ABC, abstractmethod

import httpx

from llm_client import TIMEOUT_SECONDS, ChatResult, LLMError, chat as ollama_chat


class UnsupportedParameterError(LLMError):
    """Raised when a provider can't do what was asked (e.g. context_size over the OpenAI API)."""


class LLMProvider(ABC):
    """The contract every provider follows. Only the parameters all providers share."""

    name: str  # each provider sets it, e.g. "ollama"

    @abstractmethod
    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        seed: int | None = None,
        stop: list[str] | None = None,
    ) -> ChatResult:
        """Send the messages and return the answer in the same ChatResult shape for every provider."""


def parse_openai_response(data: dict, duration_seconds: float) -> ChatResult:
    """Map an OpenAI Chat Completions response to our ChatResult. Pure: no network.

    The response has no timing breakdown (no total_duration, load or eval times),
    so the caller measures duration_seconds and the timing fields stay at 0.0.
    """
    choices = data.get("choices") or []
    if not choices:
        raise LLMError(f"No choices in the response: {data}")

    choice = choices[0]
    usage = data.get("usage") or {}
    return ChatResult(
        # content is null when the model asks for a tool call (Step 05)
        text=choice["message"]["content"] or "",
        input_tokens=usage.get("prompt_tokens", 0),
        output_tokens=usage.get("completion_tokens", 0),
        duration_seconds=duration_seconds,
        stop_reason=choice.get("finish_reason") or "unknown",
    )


class OllamaProvider(LLMProvider):
    """Ollama's native API (/api/chat) through llm_client."""

    name = "ollama"

    def __init__(self, model: str, context_size: int | None = None):
        self.model = model
        # A provider setting, not a per-request option: every num_ctx change reloads
        # the model (~1.6-1.9 s, measured in Task 4), so it stays fixed for this provider.
        self.context_size = context_size

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        seed: int | None = None,
        stop: list[str] | None = None,
    ) -> ChatResult:
        return ollama_chat(
            messages,
            self.model,
            temperature=temperature,
            max_tokens=max_tokens,
            seed=seed,
            stop=stop,
            context_size=self.context_size,
        )


class OpenAICompatibleProvider(LLMProvider):
    """Any server that speaks the OpenAI Chat Completions API (here: Ollama's /v1).

    Sent with httpx, not the openai library, so the request/response mapping stays visible.
    """

    name = "openai_compat"

    def __init__(self, base_url: str, api_key: str, model: str, context_size: int | None = None):
        if context_size is not None:
            # Fail when the app starts, not on the first request an hour later.
            raise UnsupportedParameterError(
                f"{self.name} can't set context_size: the OpenAI API has no num_ctx. "
                f"Bake it into a model instead: a Modelfile with 'FROM {model}' and "
                f"'PARAMETER num_ctx {context_size}', then 'ollama create <new-name> -f Modelfile' "
                "and use <new-name> as the model."
            )
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        seed: int | None = None,
        stop: list[str] | None = None,
    ) -> ChatResult:
        url = self.base_url + "/chat/completions"
        body = {"model": self.model, "messages": messages, "stream": False}
        # Top-level fields, not inside "options" like the native API. Skip the ones left as None.
        for key, value in {"temperature": temperature, "max_tokens": max_tokens, "seed": seed, "stop": stop}.items():
            if value is not None:
                body[key] = value
        headers = {"Authorization": f"Bearer {self.api_key}"}

        start = time.perf_counter()
        try:
            response = httpx.post(url, json=body, headers=headers, timeout=TIMEOUT_SECONDS)
        except httpx.ConnectError as e:
            raise LLMError(f"Can't reach {self.base_url}. Is the server running?") from e
        except httpx.TimeoutException as e:
            raise LLMError(f"No answer from {self.base_url} within {TIMEOUT_SECONDS}s.") from e
        # No total_duration in the response, so measure it here. It includes the HTTP round trip,
        # not only the model's time like Ollama's total_duration.
        duration = time.perf_counter() - start

        if response.status_code == 401:
            raise LLMError(f"{self.name} rejected the API key (HTTP 401). Check LLM_API_KEY.")
        if response.status_code == 404:
            raise LLMError(f"Model or endpoint not found: {self.model} at {url}")
        if response.status_code >= 400:
            raise LLMError(f"{self.name} returned HTTP {response.status_code}: {response.text}")

        return parse_openai_response(response.json(), duration)


DEFAULT_MODEL = "qwen2.5:3b"
SUPPORTED_PROVIDERS = ("ollama", "openai_compat")


def get_provider() -> LLMProvider:
    """Build the provider chosen by env vars, like Laravel's DB_CONNECTION / MAIL_MAILER.

    LLM_PROVIDER  ollama (default) | openai_compat
    LLM_MODEL     model name (default qwen2.5:3b)
    LLM_BASE_URL  openai_compat only, e.g. http://127.0.0.1:11434/v1
    LLM_API_KEY   openai_compat only. Never in code. Any value works for local Ollama.
    """
    provider = os.environ.get("LLM_PROVIDER", "ollama").strip().lower()
    model = os.environ.get("LLM_MODEL", DEFAULT_MODEL)

    if provider == "ollama":
        # The URL comes from OLLAMA_URL in llm_client (default http://127.0.0.1:11434).
        return OllamaProvider(model)

    if provider == "openai_compat":
        base_url = os.environ.get("LLM_BASE_URL")
        api_key = os.environ.get("LLM_API_KEY")
        if not base_url:
            raise LLMError(
                "LLM_PROVIDER=openai_compat needs LLM_BASE_URL, "
                'e.g. $env:LLM_BASE_URL="http://127.0.0.1:11434/v1"'
            )
        if not api_key:
            raise LLMError(
                "LLM_PROVIDER=openai_compat needs LLM_API_KEY in the environment (never in code). "
                'For local Ollama any value works: $env:LLM_API_KEY="ollama"'
            )
        return OpenAICompatibleProvider(base_url, api_key, model)

    raise LLMError(f"Unknown LLM_PROVIDER={provider!r}. Use one of: {', '.join(SUPPORTED_PROVIDERS)}")
