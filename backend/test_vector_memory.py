from app.memory.vector import VectorMemory

memory = VectorMemory()

print("Clearing old memories...")
memory.clear()

print("Adding memories...")

memory.add_memory(
    text="My name is Suprit.",
    role="user",
)

memory.add_memory(
    text="I live in Karnataka.",
    role="user",
)

memory.add_memory(
    text="I am building a Live AI Assistant.",
    role="user",
)

print("\nTotal Memories:", memory.count())

print("\nSearch 1")
print(memory.search("What is my name?"))

print("\nSearch 2")
print(memory.search("Where do I live?"))

print("\nSearch 3")
print(memory.search("What project am I building?"))