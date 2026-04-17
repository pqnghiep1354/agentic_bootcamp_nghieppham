#!/usr/bin/env python3
"""Verify that the lab environment is correctly set up."""

import sys

def check(name, test_fn):
    try:
        test_fn()
        print(f"  [OK] {name}")
        return True
    except Exception as e:
        print(f"  [FAIL] {name}: {e}")
        return False

def main_guardrails():
    print("=" * 50)
    print("  TechStore Vietnam - Guardrails Lab Setup Check")
    print("=" * 50)
    results = []

    print("\n1. Python version:")
    results.append(check(f"Python {sys.version.split()[0]}", lambda: None))

    print("\n2. Core dependencies:")
    results.append(check("openai", lambda: __import__("openai")))
    results.append(check("nemoguardrails", lambda: __import__("nemoguardrails")))
    results.append(check("dotenv", lambda: __import__("dotenv")))

    print("\n3. Optional dependencies:")
    check("jupyter", lambda: __import__("jupyter"))
    check("pytest", lambda: __import__("pytest"))

    print("\n4. API key:")
    import os
    from dotenv import load_dotenv

    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    load_dotenv(env_path)
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        results.append(check(f"OPENAI_API_KEY set (ends with ...{api_key[-6:]})", lambda: None))
    else:
        results.append(check("OPENAI_API_KEY", lambda: (_ for _ in ()).throw(ValueError("Not set! Check .env file"))))

    model = os.getenv("OPENAI_MODEL", "gpt-4.1-nano")
    print(f"  [INFO] Model: {model}")

    print("\n5. Config directories:")
    config_base = os.path.join(os.path.dirname(__file__), "..", "config")
    for d in ["01_unprotected", "02_input_rails", "03_dialog_rails", "04_output_rails", "05_full_protection"]:
        path = os.path.join(config_base, d)
        results.append(check(f"config/{d}", lambda p=path: os.path.isdir(p) or (_ for _ in ()).throw(FileNotFoundError(p))))

    print("\n6. Quick API test:")
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say OK"}],
            max_tokens=5,
        )
        answer = (resp.choices[0].message.content or "").strip()
        results.append(check(f"API call successful (response: '{answer}')", lambda: None))
    except Exception as e:
        results.append(check("API call", lambda: (_ for _ in ()).throw(e)))

    passed = sum(results)
    total = len(results)
    print(f"\n{'=' * 50}")
    print(f"  Result: {passed}/{total} checks passed")
    if passed == total:
        print("  All checks passed! You're ready to start the labs.")
    else:
        print("  Some checks failed. Please fix the issues above.")
    print(f"{'=' * 50}")

    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main_guardrails())
"""Verify environment setup for Extensible Agents Lab (v2)."""
import sys, os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def main():
    print("=" * 55)
    print("Extensible Agents Lab v2 — Environment Check")
    print("=" * 55)
    ok = True
    v = sys.version_info
    print(f"\nPython: {v.major}.{v.minor}.{v.micro}", end="")
    print(" [OK]" if v.major == 3 and v.minor >= 10 else " [WARN] 3.10+ recommended")

    for label, pkgs in [("Required", {"openai":"openai","dotenv":"python-dotenv",
        "langchain_openai":"langchain-openai","pydantic":"pydantic"}),
        ("Optional", {"langgraph":"langgraph"})]:
        print(f"\n{label} packages:")
        for imp, pip in pkgs.items():
            try: __import__(imp); print(f"  [OK] {pip}")
            except ImportError: print(f"  [MISSING] {pip}"); ok = label == "Required" and False or ok

    from dotenv import load_dotenv
    load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
    key = os.getenv("OPENAI_API_KEY", "")
    print(f"\n.env: {'[OK] ***' + key[-6:] if key else '[MISSING]'}, model={os.getenv('OPENAI_MODEL','?')}")
    db = os.path.join(PROJECT_ROOT, "db", "datatech.db")
    print(f"Database: {'[OK]' if os.path.exists(db) else '[RUN] python db/setup_database.py'}")
    print(f"Skill: {'[OK]' if os.path.exists(os.path.join(PROJECT_ROOT,'skills','kpi-report-skill','SKILL.md')) else '[MISSING]'}")

    print("\nOpenAI API: ", end="")
    try:
        from openai import OpenAI
        r = OpenAI(api_key=key).chat.completions.create(
            model=os.getenv("OPENAI_MODEL","gpt-4.1-nano"),
            messages=[{"role":"user","content":"Say OK"}], max_tokens=5)
        print(f"[OK] {r.choices[0].message.content}")
    except Exception as e: print(f"[FAILED] {e}"); ok = False

    print("\n" + "=" * 55)
    print("All checks passed!" if ok else "Fix issues above.")
    print("=" * 55)

if __name__ == "__main__":
    main()
