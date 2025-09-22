from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import StreamingResponse
import bittensor as bt
from loguru import logger
from common.protocol import ChatCompletionRequest, OrganicNonStreamSynapse, OrganicStreamSynapse, SyntheticStreamSynapse
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from neurons.validator import Validator


app = FastAPI()
router = APIRouter()

@router.post("/{cid}/chat/completions")
async def chat(cid: str, request: Request, body: ChatCompletionRequest):
    v: "Validator" = request.app.state.validator
    return await v.forward_miner(cid, body)


@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(router, prefix="/miners")
