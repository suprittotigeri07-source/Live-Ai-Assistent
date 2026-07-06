from app.agents.base import BaseAgent
from app.agents.planner import Planner

from app.llm.providers.factory import get_provider
from app.tools.manager import ToolManager


class AssistantAgent(BaseAgent):

    def __init__(self):

        self.provider = get_provider()
        self.tools = ToolManager()
        self.planner = Planner()

    def run(self, message: str):

        tool = self.planner.choose_tool(message)

        if tool:

            tool_result = self.tools.execute(tool, message)

            return {
                "type": "tool",
                "tool": tool,
                "result": tool_result,
            }

        response = self.provider.chat(message)

        return {
            "type": "llm",
            "response": response,
        }

    def stream(self, message: str):

        return self.provider.stream_chat(message)