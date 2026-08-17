from app.core.settings import settings
from app.llm.providers.ollama import OllamaProvider


def get_provider():

    if settings.LLM_PROVIDER.lower() == "ollama":
        return OllamaProvider()

    raise ValueError(
        f"Unsupported provider: {settings.LLM_PROVIDER}"
    )