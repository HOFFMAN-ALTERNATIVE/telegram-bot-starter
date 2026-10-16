from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot.config import Settings
from bot.keyboards import MenuCB, back_button, main_menu

router = Router(name="menu")

TEXTS = {
    "about": "🤖 A starter bot built with aiogram 3 — async, typed and modular.",
    "help": "Commands:\n/start — main menu\n/menu — show menu\n/ask <text> — ask the local AI",
    "ask": "💬 Send /ask followed by your question.",
}


@router.callback_query(MenuCB.filter(F.action == "home"))
async def on_home(query: CallbackQuery, settings: Settings) -> None:
    if isinstance(query.message, Message):
        await query.message.edit_text("Main menu:", reply_markup=main_menu(settings.llm_enabled))
    await query.answer()


@router.callback_query(MenuCB.filter(F.action.in_(TEXTS.keys())))
async def on_section(query: CallbackQuery, callback_data: MenuCB) -> None:
    if isinstance(query.message, Message):
        await query.message.edit_text(TEXTS[callback_data.action], reply_markup=back_button())
    await query.answer()
