from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.agents.assistant import AssistantAgent
from app.schemas.chat import ChatRequest

router = APIRouter()

agent = AssistantAgent()


@router.post("/chat")
async def chat(request: ChatRequest):

    return agent.run(request.message)


@router.post("/chat/stream")
async def stream_chat(request: ChatRequest):

    return StreamingResponse(
        agent.stream(request.message),
        media_type="text/plain",
    )