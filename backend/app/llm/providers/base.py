from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):

    @abstractmethod
    def chat(self, messages: list):
        pass

    @abstractmethod
    def stream_chat(self, messages: list):
        pass