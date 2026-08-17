from app.memory.base import BaseMemory


class ConversationMemory(BaseMemory):

    MAX_MESSAGES = 20

    def __init__(self):
        self.messages = []

    def add_message(self, role: str, content: str):

        self.messages.append(
            {
                "role": role,
                "content": content,
            }
        )

        if len(self.messages) > self.MAX_MESSAGES:
            self.messages.pop(0)

    def get_messages(self):
        return self.messages

    def clear(self):
        self.messages.clear()