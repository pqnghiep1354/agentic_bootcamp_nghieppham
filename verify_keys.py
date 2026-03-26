import logging
import os

from dotenv import load_dotenv
from google import genai
from tavily import TavilyClient


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def must_get_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


def verify_gemini() -> None:
    logger.info("Verifying Gemini API key...")
    must_get_env("GEMINI_API_KEY")
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents="Reply with exactly: OK",
    )
    logger.info("Gemini check complete")
    print(f"Gemini: {response.text}")


def verify_tavily() -> None:
    logger.info("Verifying Tavily API key...")
    api_key = must_get_env("TAVILY_API_KEY")
    tavily_client = TavilyClient(api_key=api_key)
    response = tavily_client.search("What is 2+2? Reply with a single digit.")
    logger.info("Tavily check complete")
    print(f"Tavily: got keys: {list(response.keys())}")


if __name__ == "__main__":
    logger.info("Loading .env file")
    load_dotenv()
    verify_gemini()
    verify_tavily()
    logger.info("All checks passed")
    print("All good.")
