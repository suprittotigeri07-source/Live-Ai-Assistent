from app.core.settings import settings
from app.llm.providers.ollama import OllamaProvider


def get_provider():

    providers = {
        "ollama": OllamaProvider,
    }

    provider_class = providers.get(settings.LLM_PROVIDER)

    if provider_class is None:
        raise ValueError(
            f"Unknown provider: {settings.LLM_PROVIDER}"
        )

    return provider_class()