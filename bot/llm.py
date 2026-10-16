from __future__ import annotations

import httpx


class OllamaClient:
    """Minimal async client for a local Ollama server (/api/chat, non-streaming)."""

    def __init__(
        self,
        base_url: str,
        model: str,
        timeout: float = 120.0,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.model = model
        self._client = client or httpx.AsyncClient(base_url=base_url, timeout=timeout)

    async def chat(self, prompt: str, system: str | None = None) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        resp = await self._client.post(
            "/api/chat", json={"model": self.model, "messages": messages, "stream": False}
        )
        resp.raise_for_status()
        return resp.json()["message"]["content"].strip()

    async def close(self) -> None:
        await self._client.aclose()
