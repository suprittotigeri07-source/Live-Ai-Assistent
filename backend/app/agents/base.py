from abc import ABC, abstractmethod


class BaseAgent(ABC):

    @abstractmethod
    def run(self, message: str):
        pass

    @abstractmethod
    def stream(self, message: str):
        pass