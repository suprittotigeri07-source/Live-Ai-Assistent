from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.api.dependencies import get_llm_provider
from app.schemas.chat import ChatRequest

router = APIRouter()


@router.post("/chat/stream")
async def stream_chat(
    request: ChatRequest,
    provider=Depends(get_llm_provider),
):

    return StreamingResponse(
        provider.stream_chat(request.message),
        media_type="text/plain",
    )