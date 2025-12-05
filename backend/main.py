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


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(body: ChatRequest):
    """
    Simple chat endpoint.
    Input: { "message": "your text" }
    Output: { "reply": "model response" }
    """
    completion = client.chat.completions.create(
        model="gpt-4.1-mini",  # you can change to gpt-4.1 or better if you want
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful, concise AI assistant. "
                    "Explain things simply and clearly like a tutor."
                ),
            },
            {"role": "user", "content": body.message},
        ],
        max_tokens=400,
        temperature=0.7,
    )

    reply_text = completion.choices[0].message.content
    return ChatResponse(reply=reply_text)
