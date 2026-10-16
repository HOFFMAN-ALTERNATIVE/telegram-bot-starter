from aiogram import Router

from . import ai, menu, start


def build_router() -> Router:
    root = Router(name="root")
    root.include_routers(start.router, menu.router, ai.router)
    return root
