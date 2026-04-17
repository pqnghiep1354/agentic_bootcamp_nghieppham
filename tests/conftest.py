"""Pytest configuration for guardrails tests."""

import os
import subprocess
import sys

from dotenv import load_dotenv

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

# Ensure pytest is available in the environment
try:
    import pytest
except (ImportError, ModuleNotFoundError):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pytest"])
    import pytest

# Shared fixtures for extensible agents tests.
LIB_PATH = os.path.join(PROJECT_ROOT, "lib")
sys.path.insert(0, LIB_PATH)

load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

# Ensure DB exists
from data import DB_PATH
if not os.path.exists(DB_PATH):
    sys.path.insert(0, os.path.join(PROJECT_ROOT, "db"))
    from setup_database import create_database
    create_database()

@pytest.fixture
def project_root():
    return PROJECT_ROOT

@pytest.fixture
def openai_client():
    from openai import OpenAI
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@pytest.fixture
def model():
    return os.getenv("OPENAI_MODEL", "gpt-4.1-nano")
