"""
local_llm.py — function واحدة بتكلّم LLM شغّال local على جهازك عن طريق Ollama.

Ollama بيشغّل الموديل كـ HTTP server على http://localhost:11434
فالكلام معاه مجرد POST request عادي — زي ما بتكلّم أي API من Laravel.

الموديل الافتراضي: qwen2.5:3b (صغير ~2GB، وكويس نسبياً في العربي).
تقدر تغيّره من environment variable:  OLLAMA_MODEL=llama3.2
"""

import os

import httpx  # HTTP client — شبه Http facade في Laravel

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:3b")


class LocalLLMError(Exception):
    """خطأ مفهوم بدل traceback طويل."""


def chat(messages: list[dict], model: str = MODEL) -> str:
    """
    ابعت محادثة للموديل ورجّع رده كنص.

    messages: list من {"role": "system" | "user" | "assistant", "content": "..."}
    """
    try:
        response = httpx.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": model, "messages": messages, "stream": False},
            timeout=180,  # أول request بيحمّل الموديل في الـ RAM فممكن ياخد وقت
        )
    except httpx.ConnectError:
        raise LocalLLMError(
            f"مش قادر أوصل لـ Ollama على {OLLAMA_URL}.\n"
            "اتأكد إنه متسطّب وشغّال (افتح برنامج Ollama، أو نفّذ: ollama serve)."
        ) from None

    if response.status_code == 404:
        raise LocalLLMError(
            f"الموديل '{model}' مش متنزّل عندك.\nنزّله بـ: ollama pull {model}"
        )
    response.raise_for_status()

    data = response.json()
    return data["message"]["content"]
