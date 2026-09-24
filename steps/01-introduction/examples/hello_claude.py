"""
hello_claude.py — أول API call لـ Claude.

التشغيل:
    uv run hello_claude.py
    uv run hello_claude.py "اشرحلي يعني إيه AI Engineer في جملتين"

محتاج ANTHROPIC_API_KEY في ملف .env (بص .env.example).
"""

import sys

import anthropic
from dotenv import load_dotenv

load_dotenv()  # بيقرا .env ويحط القيم في environment variables

MODEL = "claude-opus-5"  # غيّره لـ "claude-haiku-4-5" لو عايز أرخص وأسرع


def main() -> None:
    question = " ".join(sys.argv[1:]) or "عرّفني بنفسك في جملتين، وقولّي ممكن تساعد AI Engineer في إيه."

    # الـ client بيقرا ANTHROPIC_API_KEY من الـ environment لوحده — مفيش key في الكود
    client = anthropic.Anthropic()

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            messages=[{"role": "user", "content": question}],
        )
    except anthropic.AuthenticationError:
        sys.exit("❌ الـ API key غلط أو مش موجود. شغّل check_env.py الأول.")
    except anthropic.RateLimitError:
        sys.exit("⏳ عديت الـ rate limit — استنى شوية وجرّب تاني.")
    except anthropic.APIConnectionError:
        sys.exit("🌐 مش قادر أوصل للـ API — اتأكد من الإنترنت.")

    # لازم نبص على stop_reason قبل ما نقرا المحتوى
    if response.stop_reason == "refusal":
        sys.exit("🚫 الموديل رفض الطلب ده.")

    # response.content عبارة عن list من blocks — بناخد الـ text بس
    answer = "".join(block.text for block in response.content if block.type == "text")
    print(answer)

    if response.stop_reason == "max_tokens":
        print("\n⚠️  الرد اتقطع عشان وصل لـ max_tokens.")

    usage = response.usage
    print(f"\n— model: {response.model} | input tokens: {usage.input_tokens}"
          f" | output tokens: {usage.output_tokens} | stop: {response.stop_reason}")


if __name__ == "__main__":
    main()
