import os
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent_hack.agent_manager import AgentManager

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
CDP_API_KEY_NAME = os.environ["CDP_API_KEY_NAME"]
CDP_API_KEY_PRIVATE_KEY = os.environ["CDP_API_KEY_PRIVATE_KEY"]
NETWORK_ID = os.environ["NETWORK_ID"]

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_credentials=True, allow_methods=['*'], allow_headers=['*'], expose_headers=['*'], allow_origins=[
    'http://localhost:3000',
], allow_origin_regex='https://.*\\.?(tokenpage.xyz)')

agentManager = AgentManager(
    geminiApiKey=GEMINI_API_KEY,
    cdpApiKeyName=CDP_API_KEY_NAME,
    cdpApiKeyPrivateKey=CDP_API_KEY_PRIVATE_KEY,
    networkId=NETWORK_ID,
    sqliteDbPath="../secrets/checkpoints.sqlite",
)

class Message(BaseModel):
    content: str
    isUser: bool

class ChatSession(BaseModel):
    messages: List[Message]
    userId: str

class ChatRequest(BaseModel):
    content: str
    userId: str

class ChatResponse(BaseModel):
    message: Message


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    userMessage = Message(content=request.content, isUser=True)
    agentResponse = await agentManager.get_agent_response(userId=request.userId, message=userMessage.content)
    agentMessage = Message(content=agentResponse, isUser=False)
    return ChatResponse(message=agentMessage)


@app.get("/chat/{userId}", response_model=ChatSession)
async def get_chat_history(userId: str):
    messages = await agentManager.get_chat_history(userId=userId)
    return ChatSession(
        userId=userId,
        messages=[Message.model_validate(message) for message in messages],
    )
