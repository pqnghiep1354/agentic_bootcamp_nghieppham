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

def main():
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
        answer = resp.choices[0].message.content.strip()
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
    sys.exit(main())
