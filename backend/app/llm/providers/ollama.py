from openai import OpenAI

from app.core.settings import settings
from app.llm.prompts.system_prompt import SYSTEM_PROMPT
from app.llm.providers.base import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):

    def __init__(self):

        self.client = OpenAI(
            base_url=settings.OLLAMA_BASE_URL,
            api_key=settings.OLLAMA_API_KEY,
        )

    def stream_chat(self, message: str):

        stream = self.client.chat.completions.create(
            model=settings.OLLAMA_MODEL,
            stream=True,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
        )

        for chunk in stream:

            delta = chunk.choices[0].delta.content

            if delta:
                yield delta