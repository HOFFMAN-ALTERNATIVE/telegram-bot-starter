import logging

import httpx
from aiogram import Router
from aiogram.enums import ChatAction
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from bot.guard import AskGuard
from bot.llm import OllamaClient

router = Router(name="ai")
log = logging.getLogger(__name__)

SYSTEM_PROMPT = "You are a concise, helpful assistant. Answer briefly."
MAX_LEN = 4000  # Telegram message limit is 4096


@router.message(Command("ask"))
async def cmd_ask(
    message: Message, command: CommandObject, llm: OllamaClient | None, guard: AskGuard
) -> None:
    if llm is None:
        await message.answer("Local AI is disabled. Set OLLAMA_MODEL in .env to enable it.")
        return
    if not command.args:
        await message.answer("Usage: /ask <your question>")
        return
    user_id = message.from_user.id if message.from_user else None
    refused = guard.rejection(user_id, command.args)
    if refused or user_id is None:
        await message.answer(refused or "Cannot identify the sender.")
        return
    guard.acquire(user_id)
    try:
        if message.bot:
            await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        reply = await llm.chat(command.args, system=SYSTEM_PROMPT)
    except (httpx.HTTPError, KeyError, ValueError):
        log.exception("LLM request failed")
        await message.answer("The AI backend is unavailable right now.")
        return
    finally:
        guard.release(user_id)
    # Model output is untrusted text: send it without HTML parsing so stray tags
    # neither break delivery nor turn into links.
    await message.answer(reply[:MAX_LEN] or "…", parse_mode=None)
