class Planner:

    def choose_tool(self, message: str):

        msg = message.lower().strip()

        # -----------------------------
        # Web Search
        # -----------------------------
        if any(word in msg for word in [
            "latest",
            "news",
            "today",
            "current",
            "search",
            "google",
        ]):
            return "web_search"

        # -----------------------------
        # Calculator
        # -----------------------------
        if any(op in msg for op in [
            "+",
            "-",
            "*",
            "/",
        ]):
            return "calculator"

        # -----------------------------
        # No tool required
        # -----------------------------
        return None