from app.memory.conversation import ConversationMemory
from app.memory.vector import VectorMemory


class MemoryManager:

    def __init__(self):

        self.chat_memory = ConversationMemory()
        self.vector_memory = VectorMemory()

    def add_user_message(self, message: str):

        self.chat_memory.add_message(
            role="user",
            content=message,
        )

        self.vector_memory.add_memory(
            text=message,
            role="user",
        )

    def add_assistant_message(self, message: str):

        self.chat_memory.add_message(
            role="assistant",
            content=message,
        )

        self.vector_memory.add_memory(
            text=message,
            role="assistant",
        )

    def history(self):

        return self.chat_memory.get_messages()

    def retrieve(
        self,
        query: str,
        k: int = 5,
    ):

        return self.vector_memory.search(
            query,
            k,
        )

    def clear(self):

        self.chat_memory.clear()
        self.vector_memory.clear()