from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.llm.providers.factory import get_provider
from app.schemas.chat import ChatRequest

router = APIRouter()

provider = get_provider()


@router.post("/chat/stream")
async def stream_chat(request: ChatRequest):
    """
    Stream AI response token by token.
    """

    return StreamingResponse(
        provider.stream_chat(request.message),
        media_type="text/plain",
    )