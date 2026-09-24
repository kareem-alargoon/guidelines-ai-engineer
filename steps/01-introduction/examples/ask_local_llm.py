"""
ask_local_llm.py — اسأل LLM شغّال على جهازك سؤال واحد.

التشغيل:
    python ask_local_llm.py
    python ask_local_llm.py "اشرحلي يعني إيه LLM في 3 جمل"
"""

import sys

from local_llm import MODEL, LocalLLMError, chat


def main() -> None:
    question = " ".join(sys.argv[1:]) or "اشرحلي في 3 جمل بسيطة: يعني إيه Large Language Model؟"
    print(f"🧠 model: {MODEL}\n❓ {question}\n")
    try:
        answer = chat([{"role": "user", "content": question}])
    except LocalLLMError as e:
        sys.exit(f"❌ {e}")
    print(f"💬 {answer}")


if __name__ == "__main__":
    main()
