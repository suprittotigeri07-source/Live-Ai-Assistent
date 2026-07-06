import httpx

from app.core.settings import settings
from app.tools.base import BaseTool


class WebSearchTool(BaseTool):

    name = "web_search"

    description = "Searches the web for recent information."

    BASE_URL = "https://api.tavily.com/search"

    def run(self, query: str):

        payload = {
            "api_key": settings.TAVILY_API_KEY,
            "query": query,
            "search_depth": "advanced",
            "max_results": 5,
            "include_answer": True,
            "include_images": False,
        }

        try:

            response = httpx.post(
                self.BASE_URL,
                json=payload,
                timeout=30,
            )

            response.raise_for_status()

            return response.json()

        except Exception as e:

            return {
                "error": str(e)
            }