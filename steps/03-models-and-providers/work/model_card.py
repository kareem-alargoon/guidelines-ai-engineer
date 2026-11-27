import httpx
from dataclasses import dataclass
from llm_client import LLMError, OLLAMA_URL, TIMEOUT_SECONDS, send_request, handle_http_errors

BYTES_PER_GB = 1_000_000_000  # decimal GB, the same unit `ollama ls` shows


@dataclass
class ModelCard:
    name: str
    family: str
    parameter_size: str
    quantization: str
    context_length: int | None
    capabilities: list[str]
    license_name: str | None
    size_on_disk_gb: float


def fetch_local_models() -> list[dict]:
    """Raw entries from /api/tags (what `ollama ls` shows), one dict per model."""
    try:
        response = httpx.get(OLLAMA_URL + "/api/tags", timeout=TIMEOUT_SECONDS)
    except httpx.ConnectError as e:
        # Ollama is not running: no HTTP response at all, so no status_code to check.
        raise LLMError(f"Can't reach Ollama at {OLLAMA_URL}. Make sure the Ollama app is running.") from e
    except httpx.TimeoutException as e:
        raise LLMError(f"Ollama didn't answer within {TIMEOUT_SECONDS}s.") from e

    if response.status_code != 200:
        raise LLMError(f"Ollama returned HTTP {response.status_code}: {response.text}")

    return response.json()["models"]


def list_local_models() -> list[str]:
    return [model["name"] for model in fetch_local_models()]


def find_context_length(model_info: dict) -> int | None:
    # The key is "<architecture>.context_length" ("qwen2.", "llama.", "gemma3." ...),
    # so match on the ending instead of hard-coding the architecture name.
    for key, value in model_info.items():
        if key.endswith(".context_length"):
            return value
    return None


def get_size_on_disk_gb(model: str) -> float:
    # /api/show doesn't return the file size, only /api/tags does.
    # "qwen2.5" without a tag means "qwen2.5:latest", like `ollama pull` does.
    full_name = model if ":" in model else model + ":latest"
    for entry in fetch_local_models():
        if entry["name"] == full_name:
            return round(entry["size"] / BYTES_PER_GB, 2)
    return 0.0


def get_model_card(model: str) -> ModelCard:
    # Same helpers chat() uses: they turn connection, timeout and HTTP errors into LLMError.
    response = send_request(OLLAMA_URL + "/api/show", {"model": model}, TIMEOUT_SECONDS)
    handle_http_errors(response, model)
    data = response.json()

    details = data["details"]
    model_info = data["model_info"]  # flat dict: "general.license.name" is ONE key, not nested

    return ModelCard(
        name=model,
        family=details["family"],
        parameter_size=details["parameter_size"],
        quantization=details["quantization_level"],
        context_length=find_context_length(model_info),
        capabilities=data.get("capabilities", []),
        license_name=model_info.get("general.license.name"),  # not every model has it -> None
        size_on_disk_gb=get_size_on_disk_gb(model),
    )


def print_table(cards: list[ModelCard]) -> None:
    # The name column is as wide as the longest name; the others have fixed widths.
    name_width = max([len("NAME")] + [len(card.name) for card in cards]) + 2

    header = (
        f"{'NAME':<{name_width}}{'FAMILY':<10}{'PARAMS':>8}  {'QUANT':<8}"
        f"{'CONTEXT':>9}  {'LICENSE':<15}{'SIZE GB':>8}  CAPABILITIES"
    )
    print(header)
    print("-" * len(header))

    for card in cards:
        context = f"{card.context_length:,}" if card.context_length else "-"
        print(
            f"{card.name:<{name_width}}{card.family:<10}{card.parameter_size:>8}  {card.quantization:<8}"
            f"{context:>9}  {card.license_name or '-':<15}{card.size_on_disk_gb:>8.2f}  "
            f"{', '.join(card.capabilities)}"
        )


if __name__ == "__main__":
    cards = [get_model_card(name) for name in list_local_models()]
    print_table(cards)

    # A model that isn't downloaded must raise LLMError with the `ollama pull` command.
    print()
    try:
        get_model_card("not-a-real-model:1b")
    except LLMError as e:
        print(f"LLMError: {e}")
