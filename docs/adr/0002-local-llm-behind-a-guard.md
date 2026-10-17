# 0002. Local Ollama behind an in-process guard

Status: accepted
Date: 2026-10-17

## Context
`/ask` forwards a question to a language model. A cloud API means keys in config, user
messages leaving the host and a bill that grows with abuse. A local model has no bill,
but every request costs CPU or GPU time, and a Telegram bot is reachable by anyone who
finds its username.

## Options
1. Cloud LLM API with provider-side rate limits: easy, but data leaves the host and cost
   is unbounded without extra work.
2. Local Ollama, no limits: private, but one user can queue work indefinitely.
3. Local Ollama behind `AskGuard`: optional allow-list, prompt length cap, one request in
   flight per user, a global concurrency cap, and an HTTP timeout on the client.

## Decision
Option 3. It keeps data on the host and bounds the cost of a public bot with about
40 lines of code and no extra service.

## Consequences
- Model output is sent with `parse_mode=None`, so stray HTML from the model cannot break
  delivery or create links.
- Guard state is in memory: it resets on restart and is not shared across replicas.
- Requests over the global cap are refused, not queued. Users see "busy" instead of
  waiting; a queue would be the next step if that becomes annoying.
- Revisit with Redis-backed limits if the bot ever runs as more than one process.
