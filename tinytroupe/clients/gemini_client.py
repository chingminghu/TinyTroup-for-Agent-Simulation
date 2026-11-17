import os

import httpx
from openai import OpenAI

from tinytroupe import config_manager

from .openai_client import OpenAIClient


class GeminiClient(OpenAIClient):
    """Client for Gemini's OpenAI-compatible API."""

    def _count_tokens(self, messages: list, model: str):
        """Skip OpenAI/tiktoken estimation for Gemini models.

        Gemini does not use OpenAI's ChatML tokenization, so estimating it with
        tiktoken would be misleading. Actual usage is collected from the API
        response instead.
        """
        return None

    @config_manager.config_defaults(timeout="timeout")
    def _setup_from_config(self, timeout=None):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is required when API_TYPE is set to 'gemini'."
            )

        httpx_client = httpx.Client(
            timeout=httpx.Timeout(
                timeout=timeout,
                connect=10.0,
                read=timeout,
                write=10.0,
                pool=5.0,
            )
        )

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            max_retries=0,
            http_client=httpx_client,
        )
