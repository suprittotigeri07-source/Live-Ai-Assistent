import logging

from app.agents.base import BaseAgent
from app.agents.planner import Planner

from app.llm.prompts.system_prompt import SYSTEM_PROMPT
from app.llm.providers.factory import get_provider

from app.memory.manager import MemoryManager
from app.tools.manager import ToolManager

logger = logging.getLogger(__name__)


class AssistantAgent(BaseAgent):

    def __init__(self):
        self.provider = get_provider()
        self.memory = MemoryManager()
        self.tools = ToolManager()
        self.planner = Planner()

    def _build_messages(self, message: str):
        """
        Build the prompt using:
        - System Prompt
        - Retrieved Semantic Memories
        - Conversation History
        """

        relevant_memories = self.memory.retrieve(message)

        memory_context = ""

        if relevant_memories:

            memory_lines = []

            for item in relevant_memories:

                try:
                    memory_lines.append(
                        item["metadata"]["text"]
                    )

                except Exception:
                    logger.exception(
                        "Failed reading memory metadata."
                    )

            memory_context = "\n".join(memory_lines)

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

        if memory_context:

            messages.append(
                {
                    "role": "system",
                    "content":
                    (
                        "These are relevant facts remembered "
                        "from previous conversations.\n\n"
                        f"{memory_context}\n\n"
                        "Use them only if they help answer "
                        "the user's question."
                    ),
                }
            )

        messages.extend(
            self.memory.history()
        )

        return messages

    def run(self, message: str):

        try:

            logger.info("User: %s", message)

            # Save user message
            self.memory.add_user_message(message)

            # Tool Planning
            tool = self.planner.choose_tool(message)

            if tool:

                logger.info("Tool Selected: %s", tool)

                result = self.tools.execute(
                    tool,
                    message,
                )

                self.memory.add_assistant_message(
                    str(result)
                )

                return {
                    "type": "tool",
                    "tool": tool,
                    "result": result,
                }

            # Build Prompt
            messages = self._build_messages(
                message
            )

            logger.info("Sending request to LLM")

            response = self.provider.chat(
                messages
            )

            self.memory.add_assistant_message(
                response
            )

            return {
                "type": "llm",
                "response": response,
            }

        except Exception as e:

            logger.exception(e)

            return {
                "type": "error",
                "response": str(e),
            }

    def stream(self, message: str):

        self.memory.add_user_message(message)

        messages = self._build_messages(message)

        def generator():

            full_response = ""

            try:

                for chunk in self.provider.stream_chat(
                    messages
                ):

                    full_response += chunk

                    yield chunk

                self.memory.add_assistant_message(
                    full_response
                )

            except Exception as e:

                logger.exception(e)

                yield f"\nERROR: {e}"

        return generator()