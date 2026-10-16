# telegram-bot-starter

![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)
![aiogram](https://img.shields.io/badge/aiogram-3.x-2CA5E0?logo=telegram&logoColor=white)
![Ruff](https://img.shields.io/badge/lint-ruff-D7FF64)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

A clean, modern template for async Telegram bots — ready to clone, configure and ship.

- **aiogram 3** with modular routers (`start`, `menu`, `ai`)
- **Typed config** via `pydantic-settings` (`.env`, secrets as `SecretStr`)
- **Inline-keyboard main menu** using typed `CallbackData`
- **Optional local LLM** chat (`/ask`) through [Ollama](https://ollama.com) with `httpx` — no cloud API keys
- **Dependency injection** of settings and LLM client into handlers
- **Docker + Compose**, non-root container
- **Ruff** lint/format and **pytest** tests (incl. mocked HTTP)

## Quick start

```bash
git clone https://github.com/HOFFMAN-ALTERNATIVE/telegram-bot-starter.git
cd telegram-bot-starter
cp .env.example .env            # put your BOT_TOKEN from @BotFather

python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
python -m bot
```

### With Docker

```bash
docker compose up -d --build
```

### Enable local AI (optional)

```bash
ollama pull llama3.2:3b
# .env
OLLAMA_MODEL=llama3.2:3b
OLLAMA_URL=http://127.0.0.1:11434   # in Docker: http://host.docker.internal:11434
```

Keep the Ollama API bound to `127.0.0.1` — it has no authentication.

## Structure

```
bot/
  __main__.py      entry point: Bot, Dispatcher, DI, polling
  config.py        pydantic-settings
  keyboards.py     inline keyboards + CallbackData
  llm.py           async Ollama client
  handlers/
    start.py       /start, /menu
    menu.py        inline menu navigation
    ai.py          /ask → local LLM
tests/             pytest (settings, keyboards, routers, mocked LLM)
ci/ci.yml          GitHub Actions workflow (ruff + pytest)
```

Add a feature: create `bot/handlers/<feature>.py` with its own `Router`, then include it in `bot/handlers/__init__.py`.

## Development

```bash
ruff check . && ruff format --check . && pytest -q
```

## License

MIT — see [LICENSE](LICENSE).
