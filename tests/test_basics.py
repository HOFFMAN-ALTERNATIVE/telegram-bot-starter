import httpx

from bot.config import Settings
from bot.handlers import build_router
from bot.keyboards import MenuCB, main_menu
from bot.llm import OllamaClient


def _actions(markup) -> list[str]:
    return [MenuCB.unpack(b.callback_data).action for row in markup.inline_keyboard for b in row]


def test_settings_from_env(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "123:abc")
    s = Settings(_env_file=None)
    assert s.bot_token.get_secret_value() == "123:abc"
    assert not s.llm_enabled


def test_menu_hides_ai_when_disabled():
    assert "ask" in _actions(main_menu(llm_enabled=True))
    assert "ask" not in _actions(main_menu(llm_enabled=False))


def test_router_builds():
    assert {r.name for r in build_router().sub_routers} == {"start", "menu", "ai"}


async def test_ollama_client():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/chat"
        return httpx.Response(200, json={"message": {"role": "assistant", "content": " hi "}})

    client = httpx.AsyncClient(base_url="http://test", transport=httpx.MockTransport(handler))
    llm = OllamaClient("http://test", "any-model", client=client)
    assert await llm.chat("hello") == "hi"
    await llm.close()
