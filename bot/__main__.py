import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import get_settings
from bot.handlers import build_router
from bot.llm import OllamaClient


async def main() -> None:
    settings = get_settings()
    logging.basicConfig(
        level=settings.log_level, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )

    llm = (
        OllamaClient(settings.ollama_url, settings.ollama_model, settings.ollama_timeout)
        if settings.ollama_model
        else None
    )

    bot = Bot(
        settings.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(settings=settings, llm=llm)
    dp.include_router(build_router())

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        if llm:
            await llm.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
