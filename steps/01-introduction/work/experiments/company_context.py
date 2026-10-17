from pathlib import Path
from llm_client import chat, Role


here = Path(__file__).parent
work = here.parent
data = work / "data"
policy = data / "company_policy.md"
context = policy.read_text(encoding="utf-8")

system_prompt = f"""انت مساعد لموظفين شركة نَسَق. جاوب من المستند اللي تحت بس. لو الإجابة مش في المستند، قول إنك مش عارف، ومتألّفش.
<document>
{context}
</document>
"""

questions = [
    "كام يوم إجازة سنوية لموظف بقاله 3 سنين في الشركة؟",
    "ينفع أشتغل من البيت يومين الإثنين والتلات؟",
    "لو يوم 25 جه يوم جمعة، المرتب بيتصرف إمتى؟",
    "الشركة بتدّي تأمين صحي؟",
    "ينفع أستخدم ChatGPT عشان أراجع كود الشركة؟",
]

for i, question in enumerate(questions, start=1):
    print("من غير المستند: ----------------------------------------")
    chat_result = chat([{"role": Role.USER.value, "content": question}])
    print(f"السؤال ({i}): " + question)
    print(chat_result.text)

    print("بالمستند: ----------------------------------------")
    chat_result = chat([
        {"role": Role.SYSTEM.value, "content": system_prompt},
        {"role": Role.USER.value, "content": question},
    ])
    print(f"السؤال ({i}): " + question)
    print(chat_result.text)
