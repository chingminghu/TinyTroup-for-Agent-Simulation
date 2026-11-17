from unittest.mock import patch

import pytest

from tinytroupe.clients import _get_client_for_api_type
from tinytroupe.clients.gemini_client import GeminiClient


def test_gemini_client_is_registered():
    assert isinstance(_get_client_for_api_type("gemini"), GeminiClient)


def test_gemini_client_uses_openai_compatible_configuration(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-gemini-key")
    with patch("tinytroupe.clients.gemini_client.httpx.Client") as httpx_client:
        with patch("tinytroupe.clients.gemini_client.OpenAI") as openai:
            client = GeminiClient(cache_api_calls=False)
            client._setup_from_config(timeout=12)

    openai.assert_called_once_with(
        api_key="test-gemini-key",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        max_retries=0,
        http_client=httpx_client.return_value,
    )


def test_gemini_client_requires_api_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    client = GeminiClient(cache_api_calls=False)

    with pytest.raises(ValueError, match="GEMINI_API_KEY"):
        client._setup_from_config(timeout=12)


def test_gemini_client_skips_openai_token_estimation():
    client = GeminiClient(cache_api_calls=False)

    assert (
        client._count_tokens(
            [{"role": "user", "content": "hello"}], "gemini-3.8-flash"
        )
        is None
    )
