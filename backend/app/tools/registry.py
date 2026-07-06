from app.tools.base import BaseTool


class ToolRegistry:

    def __init__(self):
        self.tools = {}

    def register(self, tool: BaseTool):
        self.tools[tool.name] = tool

    def get(self, tool_name: str):
        return self.tools.get(tool_name)

    def list(self):
        return list(self.tools.values())