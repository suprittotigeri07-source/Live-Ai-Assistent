from fastapi import APIRouter

from app.agents.assistant import AssistantAgent

router = APIRouter()

agent = AssistantAgent()


@router.get("/memory")
async def get_memory():
    return agent.memory.history()


@router.post("/memory/clear")
async def clear_memory():
    agent.memory.clear()
    return {"message": "Conversation memory cleared"}