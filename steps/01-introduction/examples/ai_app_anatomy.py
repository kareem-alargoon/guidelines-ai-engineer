"""
ai_app_anatomy.py — تشريح أبسط AI app: "مُصنِّف تذاكر الدعم الفني".

الفكرة إن الـ LLM call نفسه خطوة واحدة بس من pipeline كاملة:

    input  →  validate  →  build prompt  →  call LLM  →  parse & validate output  →  result

التشغيل:
    uv run ai_app_anatomy.py --mock     # من غير API key — بيستخدم موديل وهمي
    uv run ai_app_anatomy.py            # بيكلم Claude فعلاً (محتاج .env)
"""

import json
import sys
from dataclasses import dataclass

CATEGORIES = ["billing", "technical", "account", "other"]
MAX_INPUT_CHARS = 2000


@dataclass
class TicketResult:
    category: str
    summary: str


# ── 1) Input validation ─────────────────────────────────────────────
def validate_input(text: str) -> str:
    text = text.strip()
    if not text:
        raise ValueError("التذكرة فاضية")
    if len(text) > MAX_INPUT_CHARS:
        raise ValueError(f"التذكرة أطول من {MAX_INPUT_CHARS} حرف")
    return text


# ── 2) Prompt building ──────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You classify customer support tickets. "
    f"Allowed categories: {', '.join(CATEGORIES)}. "
    'Reply with JSON only, exactly in this shape: {"category": "...", "summary": "..."}. '
    "The summary is one short sentence in the same language as the ticket."
)


def build_messages(ticket: str) -> list[dict]:
    # بنحط التذكرة جوه tags عشان نفصل كلام المستخدم عن التعليمات بتاعتنا
    return [{"role": "user", "content": f"<ticket>\n{ticket}\n</ticket>"}]


# ── 3) LLM call (حقيقي أو وهمي) ─────────────────────────────────────
def call_llm_mock(system: str, messages: list[dict]) -> str:
    """موديل وهمي بسيط عشان تفهم الـ flow من غير API key ومن غير فلوس."""
    text = messages[-1]["content"].lower()
    if any(w in text for w in ["فاتورة", "دفع", "invoice", "charge", "refund"]):
        category = "billing"
    elif any(w in text for w in ["باسورد", "password", "login", "حساب"]):
        category = "account"
    elif any(w in text for w in ["error", "crash", "مش شغال", "بيقفل"]):
        category = "technical"
    else:
        category = "other"
    return json.dumps({"category": category, "summary": "(mock) ملخص التذكرة"}, ensure_ascii=False)


def call_llm_claude(system: str, messages: list[dict]) -> str:
    import anthropic
    from dotenv import load_dotenv

    load_dotenv()
    client = anthropic.Anthropic()
    try:
        response = client.messages.create(
            model="claude-opus-5",
            max_tokens=1024,
            system=system,
            messages=messages,
        )
    except anthropic.AuthenticationError:
        sys.exit("❌ الـ API key غلط أو مش موجود. شغّل check_env.py الأول، أو جرّب --mock.")
    if response.stop_reason == "refusal":
        raise RuntimeError("الموديل رفض الطلب")
    return "".join(b.text for b in response.content if b.type == "text")


# ── 4) Output parsing & validation ──────────────────────────────────
def parse_output(raw: str) -> TicketResult:
    # الموديلات ساعات بتلف الـ JSON في ```json ... ``` — بنشيلها
    cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"الموديل رجّع حاجة مش JSON: {raw!r}") from e
    if data.get("category") not in CATEGORIES:
        # عمرك ما تثق في output الموديل من غير ما تتحقق منه
        data["category"] = "other"
    return TicketResult(category=data["category"], summary=str(data.get("summary", "")))


# ── الـ pipeline كلها ───────────────────────────────────────────────
def classify(ticket: str, llm=call_llm_mock) -> TicketResult:
    ticket = validate_input(ticket)
    messages = build_messages(ticket)
    raw = llm(SYSTEM_PROMPT, messages)
    return parse_output(raw)


if __name__ == "__main__":
    use_mock = "--mock" in sys.argv
    llm = call_llm_mock if use_mock else call_llm_claude
    print(f"الوضع: {'mock (من غير API)' if use_mock else 'Claude API'}\n")

    tickets = [
        "اتخصم مني فلوس مرتين على نفس الفاتورة الشهر ده!",
        "التطبيق بيقفل لوحده أول ما أفتح صفحة الإعدادات",
        "نسيت الباسورد ومش عارف أعمل login",
        "",  # تذكرة فاضية عشان نشوف الـ validation
    ]
    for t in tickets:
        try:
            result = classify(t, llm=llm)
            print(f"[{result.category:<9}] {t[:45]!r}\n            ↳ {result.summary}")
        except ValueError as e:
            print(f"[rejected ] {t!r} ← {e}")
