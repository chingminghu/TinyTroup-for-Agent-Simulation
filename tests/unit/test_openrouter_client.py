from unittest.mock import patch

import pytest

from tinytroupe.clients import _get_client_for_api_type
from tinytroupe.clients.openrouter_client import OpenRouterClient


def test_openrouter_client_is_registered():
    assert isinstance(_get_client_for_api_type("openrouter"), OpenRouterClient)


def test_openrouter_client_uses_openai_compatible_configuration(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter-key")
    with patch("tinytroupe.clients.openrouter_client.httpx.Client") as httpx_client:
        with patch("tinytroupe.clients.openrouter_client.OpenAI") as openai:
            client = OpenRouterClient(cache_api_calls=False)
            client._setup_from_config(timeout=12)

    openai.assert_called_once_with(
        api_key="test-openrouter-key",
        base_url="https://openrouter.ai/api/v1",
        max_retries=0,
        http_client=httpx_client.return_value,
    )


def test_openrouter_client_requires_api_key(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    client = OpenRouterClient(cache_api_calls=False)

    with pytest.raises(ValueError, match="OPENROUTER_API_KEY"):
        client._setup_from_config(timeout=12)


def test_openrouter_client_skips_openai_token_estimation():
    client = OpenRouterClient(cache_api_calls=False)

    assert (
        client._count_tokens(
            [{"role": "user", "content": "hello"}], "provider/model"
        )
        is None
    )


