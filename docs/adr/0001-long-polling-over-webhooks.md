# 0001. Long polling instead of webhooks

Status: accepted
Date: 2026-10-17

## Context
The starter should run on a laptop, a home server or a small VPS with one command.
Webhooks need a public HTTPS endpoint, a certificate and usually a reverse proxy.

## Options
1. Webhooks: lower latency, scale horizontally behind a load balancer, but need public
   ingress and TLS, and open an attack surface.
2. Long polling via `dp.start_polling`: outbound connections only, works behind NAT,
   one process per token.

## Decision
Option 2. Zero inbound exposure and no infrastructure beats the latency gain for the
bots this template is for.

## Consequences
- The container needs no published port and can run read-only with all capabilities
  dropped.
- Only one instance per bot token can poll; scaling out means switching to webhooks.
- aiogram handles SIGTERM/SIGINT and stops polling; `main()` then closes the HTTP
  sessions in `finally`.
- Revisit when traffic needs more than one process.
