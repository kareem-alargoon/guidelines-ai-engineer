"""
check_env.py — اتأكد إن البيئة جاهزة قبل أول API call.

التشغيل:
    uv run check_env.py        (أو)  python check_env.py

بيتأكد من:
  1. نسخة Python (الـ anthropic SDK 1.x محتاج 3.10+)
  2. الـ packages المطلوبة متسطّبة
  3. ملف .env موجود ومقروء
  4. ANTHROPIC_API_KEY موجود وشكله منطقي — من غير ما يطبعه أبداً
"""

import importlib.util
import os
import sys
from pathlib import Path

OK, FAIL, WARN = "✅", "❌", "⚠️ "


def check_python() -> bool:
    v = sys.version_info
    ok = v >= (3, 10)
    print(f"{OK if ok else FAIL} Python {v.major}.{v.minor}.{v.micro}"
          + ("" if ok else "  ← محتاج 3.10 أو أحدث"))
    return ok


def check_packages() -> bool:
    all_ok = True
    for pkg, import_name in [("anthropic", "anthropic"), ("python-dotenv", "dotenv")]:
        found = importlib.util.find_spec(import_name) is not None
        all_ok &= found
        print(f"{OK if found else FAIL} package: {pkg}"
              + ("" if found else f"  ← نفّذ: uv add {pkg}"))
    return all_ok


def mask(secret: str) -> str:
    """اعرض أول وآخر كام حرف بس — عمرك ما تطبع key كامل في log."""
    return f"{secret[:7]}...{secret[-4:]}" if len(secret) > 12 else "***"


def check_api_key() -> bool:
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv(env_file)
        print(f"{OK} لقيت ملف .env")
    else:
        print(f"{WARN} مفيش ملف .env هنا — هنعتمد على environment variables النظام")

    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        print(f"{FAIL} ANTHROPIC_API_KEY مش موجود  ← انسخ .env.example لـ .env وحط الـ key")
        return False
    if not key.startswith("sk-ant-"):
        print(f"{WARN} ANTHROPIC_API_KEY موجود ({mask(key)}) بس شكله مش زي keys Anthropic المعتادة")
        return True
    print(f"{OK} ANTHROPIC_API_KEY موجود ({mask(key)})")
    return True


def main() -> int:
    print("— فحص البيئة —")
    results = [check_python(), check_packages()]
    # فحص الـ key محتاج python-dotenv، فبنعمله بس لو الـ packages موجودة
    results.append(check_api_key() if results[1] else False)
    if all(results):
        print("\n🎉 البيئة جاهزة. جرّب: uv run hello_claude.py")
        return 0
    print("\n🔧 فيه حاجات محتاجة تتظبط (بص على ❌ فوق).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
