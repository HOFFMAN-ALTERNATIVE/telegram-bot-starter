"""Access and abuse limits for the /ask command.

A public bot is reachable by every Telegram user, and each /ask costs CPU on the
Ollama host. The guard keeps that cost bounded: an optional allow-list, a prompt
length cap, at most one in-flight request per user and a global cap on
concurrent requests, so many users at once cannot queue unbounded work.
"""

from __future__ import annotations

from collections.abc import Iterable


class AskGuard:
    def __init__(
        self,
        allowed_user_ids: Iterable[int] = (),
        max_prompt_chars: int = 2000,
        max_concurrent: int = 2,
    ) -> None:
        self.allowed = frozenset(allowed_user_ids)
        self.max_prompt_chars = max_prompt_chars
        self.max_concurrent = max_concurrent
        self._busy: set[int] = set()

    def rejection(self, user_id: int | None, prompt: str) -> str | None:
        """Return a message explaining why the request is refused, or None if it may run."""
        if user_id is None:
            return "Cannot identify the sender."
        if self.allowed and user_id not in self.allowed:
            return "This command is limited to approved users."
        if len(prompt) > self.max_prompt_chars:
            return f"Question too long ({len(prompt)} characters, limit {self.max_prompt_chars})."
        if user_id in self._busy:
            return "Still working on your previous question."
        if len(self._busy) >= self.max_concurrent:
            return "The AI backend is busy. Try again in a minute."
        return None

    def acquire(self, user_id: int) -> None:
        self._busy.add(user_id)

    def release(self, user_id: int) -> None:
        self._busy.discard(user_id)
