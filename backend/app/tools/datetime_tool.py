from datetime import datetime

from app.tools.base import BaseTool


class DateTimeTool(BaseTool):

    name = "datetime"

    description = "Returns the current date and time."

    def run(self):

        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
        }