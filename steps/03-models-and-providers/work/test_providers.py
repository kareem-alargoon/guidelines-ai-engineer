"""Quick checks for parse_openai_response, get_provider and UnsupportedParameterError. No Ollama needed.

Run from the work folder:  python test_providers.py
"""
import os

from llm_client import LLMError
from providers import (
    OllamaProvider,
    OpenAICompatibleProvider,
    UnsupportedParameterError,
    get_provider,
    parse_openai_response,
)


def openai_response(content: str | None, finish_reason: str, usage: dict | None = None) -> dict:
    """A response shaped like Ollama's /v1/chat/completions (captured in Task 5)."""
    data = {
        "id": "chatcmpl-730",
        "object": "chat.completion",
        "model": "qwen2.5:3b",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": finish_reason,
            }
        ],
    }
    if usage is not None:
        data["usage"] = usage
    return data


USAGE = {"prompt_tokens": 35, "prompt_tokens_details": {"cached_tokens": 34}, "completion_tokens": 4, "total_tokens": 39}

# 1. Normal answer: every field is mapped, and duration is the one we measured.
result = parse_openai_response(openai_response("Hi there!", "stop", USAGE), duration_seconds=0.42)
assert result.text == "Hi there!"
assert result.input_tokens == 35
assert result.output_tokens == 4
assert result.stop_reason == "stop"
assert result.duration_seconds == 0.42
# No timing breakdown in the OpenAI response, so these stay at their defaults.
assert result.load_seconds == 0.0 and result.eval_seconds == 0.0
assert result.output_tokens_per_second == 0.0

# 2. Cut by max_tokens: finish_reason "length", even when the text looks complete.
cut_usage = {"prompt_tokens": 35, "completion_tokens": 3, "total_tokens": 38}
result = parse_openai_response(openai_response("Hi there!", "length", cut_usage), duration_seconds=0.3)
assert result.stop_reason == "length"
assert result.output_tokens == 3

# 3. No usage block: tokens fall back to 0 instead of crashing.
result = parse_openai_response(openai_response("Hi", "stop"), duration_seconds=0.1)
assert result.input_tokens == 0 and result.output_tokens == 0

# 3b. content is null (a tool call answer): text becomes "".
result = parse_openai_response(openai_response(None, "tool_calls", USAGE), duration_seconds=0.1)
assert result.text == ""
assert result.stop_reason == "tool_calls"

# 4. Empty choices: a clear LLMError, not an IndexError.
try:
    parse_openai_response({"choices": [], "usage": USAGE}, duration_seconds=0.1)
except LLMError as e:
    assert "No choices" in str(e)
else:
    raise AssertionError("Empty choices should raise LLMError")


# --- get_provider(): the factory reads env vars ---

ENV_VARS = ("LLM_PROVIDER", "LLM_MODEL", "LLM_BASE_URL", "LLM_API_KEY")


def provider_from_env(**env: str):
    """Call get_provider() with only these LLM_* vars set, then restore the real environment."""
    saved = {name: os.environ.get(name) for name in ENV_VARS}
    try:
        for name in ENV_VARS:
            os.environ.pop(name, None)
        os.environ.update(env)
        return get_provider()
    finally:
        for name, value in saved.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


def raises_llm_error(**env: str) -> str:
    """Return the LLMError message get_provider() raises for this env, or fail."""
    try:
        provider_from_env(**env)
    except LLMError as e:
        return str(e)
    raise AssertionError(f"Expected LLMError for {env}")


# 5. Nothing set: Ollama native with the default model.
provider = provider_from_env()
assert isinstance(provider, OllamaProvider)
assert provider.model == "qwen2.5:3b"

# 5b. openai_compat with everything set (no request is sent, only the object is built).
provider = provider_from_env(LLM_PROVIDER=" OpenAI_Compat ", LLM_MODEL="qwen2.5-3b-8k",
                             LLM_BASE_URL="http://127.0.0.1:11434/v1/", LLM_API_KEY="ollama")
assert isinstance(provider, OpenAICompatibleProvider)
assert provider.model == "qwen2.5-3b-8k"
assert provider.base_url == "http://127.0.0.1:11434/v1"  # trailing slash removed

# 6. openai_compat without a key: a clear error that names the variable.
message = raises_llm_error(LLM_PROVIDER="openai_compat", LLM_BASE_URL="http://127.0.0.1:11434/v1")
assert "LLM_API_KEY" in message

# 6b. openai_compat without a base URL.
assert "LLM_BASE_URL" in raises_llm_error(LLM_PROVIDER="openai_compat", LLM_API_KEY="ollama")

# 7. Unknown provider: the error lists the allowed values.
message = raises_llm_error(LLM_PROVIDER="olama")
assert "'olama'" in message and "ollama" in message and "openai_compat" in message

# 8. context_size over the OpenAI API fails in the constructor, and the message gives the fix.
try:
    OpenAICompatibleProvider("http://127.0.0.1:11434/v1", "ollama", "qwen2.5:3b", context_size=8192)
except UnsupportedParameterError as e:
    assert "Modelfile" in str(e)
    assert isinstance(e, LLMError)  # one except LLMError still catches it
else:
    raise AssertionError("context_size should raise UnsupportedParameterError")

print("All provider tests passed")
