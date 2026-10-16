from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MenuCB(CallbackData, prefix="menu"):
    action: str


MAIN_MENU: tuple[tuple[str, str], ...] = (
    ("📘 About", "about"),
    ("💬 Ask AI", "ask"),
    ("❓ Help", "help"),
)


def main_menu(llm_enabled: bool = True) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for text, action in MAIN_MENU:
        if action == "ask" and not llm_enabled:
            continue
        kb.button(text=text, callback_data=MenuCB(action=action))
    kb.adjust(2)
    return kb.as_markup()


def back_button() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Back", callback_data=MenuCB(action="home"))
    return kb.as_markup()
