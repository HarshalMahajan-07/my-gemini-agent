import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

# Read API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI(
    title="My Gemini-like AI Agent",
    description="Simple FastAPI backend for a GPT-based chat agent.",
    version="1.0.0",
)

# Allow your frontend (Vercel) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.get("/")
async def root():
    return {"status": "ok", "message": "AI agent backend is running."}


from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(body: ChatRequest):

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=body.message,
        system="You are a helpful, concise AI assistant.",
        max_output_tokens=400
    )

    reply_text = response.output[0].content[0].text

    return ChatResponse(reply=reply_text)
