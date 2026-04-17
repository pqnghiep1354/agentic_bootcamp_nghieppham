#!/usr/bin/env python3
"""TechStore Vietnam — Bot KHÔNG guardrails (interactive)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "attacks"))
from agents import build_unprotected_agent, chat

def main():
    print("=" * 60)
    print("  TechStore Vietnam — KHÔNG Guardrails")
    print("  User: TS-VN-001 (Nguyễn Văn An)")
    print("  Type 'quit' to exit\n")
    agent = build_unprotected_agent()
    while True:
        msg = input("\nBạn: ").strip()
        if not msg: continue
        if msg.lower() == "quit": break
        r, t, _, sid = chat(agent, msg, user_id="TS-VN-001")
        if t: print(f"[Tools: {[x['name'] for x in t]}]")
        print(f"Bot: {r}")
        print(f"[Langfuse session: {sid}]")

if __name__ == "__main__":
    main()
