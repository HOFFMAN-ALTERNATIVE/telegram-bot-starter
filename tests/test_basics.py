import httpx

from bot.config import Settings
from bot.guard import AskGuard
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


def test_settings_parse_allow_list(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "123:abc")
    monkeypatch.setenv("ASK_ALLOWED_USER_IDS", "[42, 7]")
    assert Settings(_env_file=None).ask_allowed_user_ids == [42, 7]


def test_guard_allow_list_length_and_one_request_per_user():
    g = AskGuard(allowed_user_ids=[1], max_prompt_chars=10)
    assert g.rejection(None, "hi") is not None
    assert "approved" in (g.rejection(2, "hi") or "")
    assert "too long" in (g.rejection(1, "x" * 11) or "")
    assert g.rejection(1, "hi") is None
    g.acquire(1)
    assert "previous" in (g.rejection(1, "hi") or "")
    g.release(1)
    assert g.rejection(1, "hi") is None


def test_guard_without_allow_list_accepts_anyone():
    assert AskGuard().rejection(999, "hello") is None


def test_guard_global_concurrency_cap():
    g = AskGuard(max_concurrent=2)
    g.acquire(1)
    g.acquire(2)
    assert "busy" in (g.rejection(3, "hi") or "")
    g.release(1)
    assert g.rejection(3, "hi") is None
