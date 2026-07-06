from pathlib import Path

from app.tools.base import BaseTool


class FileReaderTool(BaseTool):

    name = "file_reader"

    description = "Reads text files."

    def run(self, path: str):

        file = Path(path)

        if not file.exists():
            return "File not found."

        return file.read_text(encoding="utf-8")