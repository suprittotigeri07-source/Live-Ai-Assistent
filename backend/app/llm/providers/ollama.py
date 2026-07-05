import logging

from openai import OpenAI

from app.core.settings import settings
from app.llm.providers.base import BaseLLMProvider

logger = logging.getLogger(__name__)


class OllamaProvider(BaseLLMProvider):

    def __init__(self):

        self.client = OpenAI(
            base_url=settings.OLLAMA_BASE_URL,
            api_key=settings.OLLAMA_API_KEY,
        )

    def stream_chat(self, message: str):

        logger.info("Streaming from Ollama")

        stream = self.client.chat.completions.create(
            model=settings.OLLAMA_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are Live AI Assistant."
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            stream=True
        )

        for chunk in stream:

            delta = chunk.choices[0].delta.content

            if delta:
                yield delta