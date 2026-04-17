#!/usr/bin/env python3
"""TechStore Vietnam — Bot CÓ guardrails (interactive)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "attacks"))
from agents import build_protected_agent, chat

def main():
    print("=" * 60)
    print("  TechStore Vietnam — CÓ NeMo Guardrails")
    print("  User: TS-VN-001 | Input Rail + Output Rail active")
    print("  Type 'quit' to exit\n")
    agent = build_protected_agent()
    while True:
        msg = input("\nBạn: ").strip()
        if not msg: continue
        if msg.lower() == "quit": break
        r, t, bl, sid = chat(agent, msg, user_id="TS-VN-001")
        if bl: print(f"[BLOCKED by {bl}]")
        if t: print(f"[Tools: {[x['name'] for x in t]}]")
        print(f"Bot: {r}")
        print(f"[Langfuse session: {sid}]")

if __name__ == "__main__":
    main()
