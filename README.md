# Bootcamp Setup (uv + Gemini + Tavily + LangChain/LangGraph)

This setup is ordered for students:

1. Install `uv`
2. Use `uv` to set up project dependencies
3. Create API keys and `.env`
4. Run the verification script at the end

---

## 1) Install `uv` first (Windows / macOS / Linux)

`uv` is the package and run tool used for this course.

### macOS / Linux (recommended installer)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

If `curl` is not available:

```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

### Windows (PowerShell, recommended installer)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Confirm installation

```bash
uv --version
```

---

## 2) Use `uv` to set up the Python project

From the project root:

```bash
uv init
```

Add the libraries used in this bootcamp:

```bash
uv add langchain langgraph google-genai langchain-openai tavily-python python-dotenv
```

What these are for:

- `langchain` and `langgraph`: LLM app and workflow framework
- `google-genai`: Gemini API SDK
- `langchain-openai`: OpenAI API SDK (optional — needed if you choose OpenAI as your model provider)
- `tavily-python`: Tavily search SDK
- `python-dotenv`: load keys from `.env`

### Run Python scripts with `uv`

Use this format:

```bash
uv run python your_script.py
```

For this repo, you will run:

```bash
uv run python verify_keys.py
```

---

## 3) Prepare API keys and `.env`

### A) Gemini key from Google AI Studio

1. Open `https://aistudio.google.com/` and sign in.
2. Go to **Dashboard** -> **Projects**.
3. Make sure you have an active Google Cloud project for Gemini:
   - If this is your first time, create a new project in AI Studio.
   - If you already have a Google Cloud project, click **Import projects** and import it.
4. Open `https://aistudio.google.com/app/apikey`.
5. Select that project, then create the API key.
6. Copy the key.

### B) Tavily key

1. Open `https://app.tavily.com/`
2. Sign in or create account
3. Copy API key (usually starts with `tvly-`)

### C) OpenAI key (optional — only needed if you choose OpenAI as your model provider)

1. Open `https://platform.openai.com/api-keys` and sign in.
2. Click **Create new secret key**, give it a name, and click **Create**.
3. Copy the key immediately — it is only shown once (starts with `sk-`).
4. Make sure your account has a positive credit balance at `https://platform.openai.com/settings/organization/billing`.

### D) Create `.env` in project root

Create `.env`:

```bash
touch .env
```

Add your keys (include `OPENAI_API_KEY` only if you plan to use OpenAI):

```dotenv
GEMINI_API_KEY=YOUR_GEMINI_KEY_HERE
TAVILY_API_KEY=tvly-YOUR_TAVILY_KEY_HERE
OPENAI_API_KEY=sk-YOUR_OPENAI_KEY_HERE
```

Important:

- Keep keys in `.env` for this project only
- Do **not** commit `.env`

---

## 4) Optional manual key checks with `curl`

If you want to manually test keys before Python script:

### Load `.env` into current terminal

macOS/Linux:

```bash
set -a
source .env
set +a
```

Windows (PowerShell):

```powershell
Get-Content .env | ForEach-Object {
  if ($_ -match '^\s*([^#][^=]+)=(.*)\s*$') {
    [Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process')
  }
}
```

### Gemini check

macOS/Linux:

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H 'Content-Type: application/json' \
  -X POST \
  -d '{"contents":[{"parts":[{"text":"Reply with exactly: OK"}]}]}'
```

Windows (PowerShell):

```powershell
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent" `
  -H "x-goog-api-key: $env:GEMINI_API_KEY" `
  -H "Content-Type: application/json" `
  -X POST `
  -d '{\"contents\":[{\"parts\":[{\"text\":\"Reply with exactly: OK\"}]}]}'
```

### Tavily check

macOS/Linux:

```bash
curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TAVILY_API_KEY" \
  -d '{"query":"Reply with one fact about the Eiffel Tower"}'
```

Windows (PowerShell):

```powershell
curl -X POST https://api.tavily.com/search `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer $env:TAVILY_API_KEY" `
  -d '{\"query\":\"Reply with one fact about the Eiffel Tower\"}'
```

---

## 5) Final step: run `verify_keys.py`

`verify_keys.py` is already included in this repository.

From project root:

```bash
uv run python verify_keys.py
```

Expected output includes:

- `INFO: Loading .env file`
- `Gemini: OK`
- `Tavily: got keys: [...]`
- `All good.`

---

## Troubleshooting

### “Command not found: uv”

- Restart terminal and run `uv --version` again

### “401 Unauthorized” / “API key not valid”

- Check `.env` values for extra spaces
- Confirm `.env` is in the project root

### Python import errors

- Re-run dependency install: `uv add langchain langgraph google-genai langchain-openai tavily-python python-dotenv`
- Then re-run: `uv run python verify_keys.py`

