from app.tools.calculator import CalculatorTool
from app.tools.datetime_tool import DateTimeTool
from app.tools.file_reader import FileReaderTool
from app.tools.registry import ToolRegistry
from app.tools.web_search import WebSearchTool


class ToolManager:

    def __init__(self):

        self.registry = ToolRegistry()

        self.registry.register(DateTimeTool())
        self.registry.register(CalculatorTool())
        self.registry.register(FileReaderTool())
        self.registry.register(WebSearchTool())

    def execute(self, tool_name: str, *args):

        tool = self.registry.get(tool_name)

        if tool is None:
            raise ValueError(f"Tool '{tool_name}' not found.")

        return tool.run(*args)