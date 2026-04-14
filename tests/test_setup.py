"""Test lab environment setup."""

import os
import pytest
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

def test_openai_installed():
    import openai
    assert openai.__version__

def test_nemoguardrails_installed():
    import nemoguardrails

def test_langgraph_installed():
    import langgraph

def test_langfuse_installed():
    import langfuse

def test_api_key_set():
    assert os.getenv("OPENAI_API_KEY", "").startswith("sk-")

def test_guardrails_config_exists():
    config = os.path.join(os.path.dirname(__file__), "..", "config", "guardrails")
    assert os.path.isdir(config)
    assert os.path.isfile(os.path.join(config, "config.yml"))
    assert os.path.isfile(os.path.join(config, "prompts.yml"))

def test_database_setup():
    db = os.path.join(os.path.dirname(__file__), "..", "db", "techstore.db")
    assert os.path.isfile(db)

def test_notebooks_exist():
    nb_dir = os.path.join(os.path.dirname(__file__), "..", "notebooks")
    nbs = [f for f in os.listdir(nb_dir) if f.endswith(".ipynb")]
    assert len(nbs) >= 2, f"Expected >= 2 notebooks, found {len(nbs)}: {nbs}"

def test_agent_modules_exist():
    attacks = os.path.join(os.path.dirname(__file__), "..", "attacks")
    assert os.path.isfile(os.path.join(attacks, "agents.py"))
    assert os.path.isfile(os.path.join(attacks, "agent_tools.py"))
