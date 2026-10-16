from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from bot.config import Settings
from bot.keyboards import main_menu

router = Router(name="start")

WELCOME = "👋 Hi, {name}! Choose an option below."


@router.message(CommandStart())
async def cmd_start(message: Message, settings: Settings) -> None:
    name = message.from_user.first_name if message.from_user else "there"
    await message.answer(WELCOME.format(name=name), reply_markup=main_menu(settings.llm_enabled))


@router.message(Command("menu"))
async def cmd_menu(message: Message, settings: Settings) -> None:
    await message.answer("Main menu:", reply_markup=main_menu(settings.llm_enabled))
