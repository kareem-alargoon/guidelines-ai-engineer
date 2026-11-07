from llm_client import OLLAMA_URL, OLLAMA_MODEL, TIMEOUT_SECONDS, send_request, handle_http_errors


SENTENCES = [
    {
        "en": "Your order has been shipped.",
        "msa": "تم شحن طلبك.",
        "egy": "طلبك اتشحن.",
    },
    {
        "en": "Payment failed. Please try again.",
        "msa": "فشلت عملية الدفع. يرجى المحاولة مرة أخرى.",
        "egy": "الدفع ما نجحش. جرّب تاني لو سمحت.",
    },
    {
        "en": "When will my order arrive?",
        "msa": "متى سيصل طلبي؟",
        "egy": "الأوردر بتاعي هيوصل إمتى؟",
    },
    {
        "en": "You can return the product within 14 days of delivery if it is unused and in its original packaging.",
        "msa": "يمكنك إرجاع المنتج خلال 14 يومًا من الاستلام إذا كان غير مستخدم وفي عبوته الأصلية.",
        "egy": "تقدر ترجّع المنتج خلال 14 يوم من الاستلام لو ما استخدمتوش وفي علبته الأصلية.",
    },
    {
        "en": "The password must be at least 8 characters long.",
        "msa": "يجب ألا تقل كلمة المرور عن 8 أحرف.",
        "egy": "الباسورد لازم يكون 8 حروف على الأقل.",
    },
    {
        "en": "Hi, I ordered a blue shirt but received a red one. Can you exchange it for me?",
        "msa": "مرحبًا، طلبت قميصًا أزرق لكنني استلمت قميصًا أحمر. هل يمكنكم استبداله لي؟",
        "egy": "أهلاً، أنا طلبت قميص أزرق بس وصلني أحمر. ممكن تبدّلوهولي؟",
    },
    {
        "en": "Thank you for contacting us. A support agent will reply within 24 hours.",
        "msa": "شكرًا لتواصلك معنا. سيرد عليك أحد موظفي الدعم خلال 24 ساعة.",
        "egy": "شكراً إنك كلمتنا. حد من خدمة العملاء هيرد عليك خلال 24 ساعة.",
    },
    {
        "en": "Free shipping on orders over 500 EGP.",
        "msa": "الشحن مجاني للطلبات التي تزيد قيمتها عن 500 جنيه.",
        "egy": "الشحن ببلاش لو الأوردر فوق 500 جنيه.",
    },
]


def count_tokens(text: str, model: str | None = None) -> int:
    """Count the number of tokens in a string."""
    model = model or OLLAMA_MODEL
    url = OLLAMA_URL + "/api/generate"

    response = send_request(url,
                            {"model": model, "prompt": text, "raw": True, "stream": False,
                             "options": {"num_predict": 1}},
                            TIMEOUT_SECONDS)

    handle_http_errors(response, model)

    data = response.json()
    return data["prompt_eval_count"]


if __name__ == "__main__":
    LABEL_WIDTH = 30
    msa_ratios = []
    egy_ratios = []

    print(f"{'Sentence':<{LABEL_WIDTH}} {'EN':>5} {'MSA':>5} {'EGY':>5} {'MSA/EN':>8} {'EGY/EN':>8}")
    print("-" * (LABEL_WIDTH + 36))

    for sentence in SENTENCES:
        en_count = count_tokens(sentence["en"])
        msa_count = count_tokens(sentence["msa"])
        egy_count = count_tokens(sentence["egy"])

        msa_ratio = msa_count / en_count
        egy_ratio = egy_count / en_count
        msa_ratios.append(msa_ratio)
        egy_ratios.append(egy_ratio)

        label = sentence["en"][:LABEL_WIDTH]
        print(f"{label:<{LABEL_WIDTH}} {en_count:>5} {msa_count:>5} {egy_count:>5} {msa_ratio:>8.2f} {egy_ratio:>8.2f}")

    msa_average = sum(msa_ratios) / len(msa_ratios)
    egy_average = sum(egy_ratios) / len(egy_ratios)

    print("-" * (LABEL_WIDTH + 36))
    print(f"{'Average':<{LABEL_WIDTH}} {'':>5} {'':>5} {'':>5} {msa_average:>8.2f} {egy_average:>8.2f}")
