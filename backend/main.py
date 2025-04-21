from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi import FastAPI
from pydantic import BaseModel
from ollama import Client, Message

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OLLAMA_API_URL = "http://localhost:11434/api/generate"


class ChatPayload(BaseModel):
    messages: list
    model: str


@app.post("/query_llm_stream")
async def query_llm_stream(payload: ChatPayload):

    client = Client()

    # Convert message into proper Ollama format
    message_objs = [
        Message(role=m["role"], content=m["content"]) for m in payload.messages
    ]

    # streaming response
    response_stream = client.chat(
        model=payload.model,
        messages=message_objs,
        stream=True,
    )

    def stream_chunks():
        for part in response_stream:
            yield part["message"]["content"]

    return StreamingResponse(stream_chunks(), media_type="text/plain")
