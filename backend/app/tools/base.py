from abc import ABC, abstractmethod


class BaseTool(ABC):
    """
    Base class for every tool.
    """

    name: str
    description: str

    @abstractmethod
    def run(self, *args, **kwargs):
        """
        Execute tool.
        """
        pass