"""NeMo Guardrails custom actions — PII detection cho Output Rail.

File này được import trực tiếp bởi agents.py:
    from config.guardrails.actions import detect_pii
"""
import re


def detect_pii(text: str) -> dict:
    """Phát hiện PII trong text bằng regex.

    Returns:
        {"has_pii": bool, "found": [("type", "value"), ...], "redacted": str}
    """
    patterns = {
        "EMAIL": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}\b',
        "PHONE_VN": r'\b0\d{9,10}\b',
        "CCCD": r'\b\d{12}\b',
    }
    found = []
    redacted = text
    for pii_type, pattern in patterns.items():
        for m in re.findall(pattern, text):
            found.append((pii_type, m))
            redacted = redacted.replace(m, f"[{pii_type}]")

    return {"has_pii": len(found) > 0, "found": found, "redacted": redacted}
