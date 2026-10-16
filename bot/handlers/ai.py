import logging

import httpx
from aiogram import Router
from aiogram.enums import ChatAction
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from bot.llm import OllamaClient

router = Router(name="ai")
log = logging.getLogger(__name__)

SYSTEM_PROMPT = "You are a concise, helpful assistant. Answer briefly."
MAX_LEN = 4000  # Telegram message limit is 4096


@router.message(Command("ask"))
async def cmd_ask(message: Message, command: CommandObject, llm: OllamaClient | None) -> None:
    if llm is None:
        await message.answer("Local AI is disabled. Set OLLAMA_MODEL in .env to enable it.")
        return
    if not command.args:
        await message.answer("Usage: /ask <your question>")
        return
    if message.bot:
        await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    try:
        reply = await llm.chat(command.args, system=SYSTEM_PROMPT)
    except httpx.HTTPError:
        log.exception("LLM request failed")
        await message.answer("⚠️ The AI backend is unavailable right now.")
        return
    await message.answer(reply[:MAX_LEN] or "…")
