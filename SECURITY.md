# Security policy

## Reporting
Use GitHub "Report a vulnerability" on this repository to open a private advisory.
Please do not open public issues for security problems. First answer within 5 working days.

## Supported versions
Only `main` receives fixes.

## Threat model
- Assets: the bot token, the Ollama host's compute, the server the bot runs on.
- Actors: any Telegram user who finds the bot.
- Entry points: messages and callback queries from Telegram; configuration from `.env`.
- Risks and mitigations:
  - Token leak: loaded as `SecretStr`, never logged; `.env` is git-ignored and only
    `.env.example` is committed.
  - Compute abuse via `/ask`: optional `ASK_ALLOWED_USER_IDS` allow-list (startup warning
    when unset), prompt length cap, one request per user, global concurrency cap,
    `OLLAMA_TIMEOUT` on every call.
  - Unauthenticated Ollama API: keep it on `127.0.0.1`; the bot reaches it via
    `host.docker.internal` in Compose.
  - Markup injection from model output: replies are sent as plain text (`parse_mode=None`).
  - Error leakage: backend failures are logged server-side; users get a generic message.
  - Container: non-root user (uid 10001), read-only root filesystem, all capabilities
    dropped, `no-new-privileges`, no published ports.
- Supply chain: CI runs `pip-audit` on the resolved dependency set on every push.
