import base64
import os
from typing import Annotated

from core import logging
from core.exceptions import UnauthorizedException
from eth_account.messages import encode_defunct
from fastapi import FastAPI
from fastapi import Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from web3 import Web3

from agent_hack.agent_manager import AgentManager

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
CDP_API_KEY_NAME = os.environ["CDP_API_KEY_NAME"]
CDP_API_KEY_PRIVATE_KEY = os.environ["CDP_API_KEY_PRIVATE_KEY"]
NETWORK_ID = os.environ["NETWORK_ID"]

logging.basicConfig(level=logging.INFO)
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_credentials=True, allow_methods=['*'], allow_headers=['*'], expose_headers=['*'], allow_origins=[
    'http://localhost:3000',
    'https://demo.yieldseeker.xyz',
    'https://app.yieldseeker.xyz',
], allow_origin_regex='https://.*\\.?(yieldseeker.xyz)')

agentManager = AgentManager(
    geminiApiKey=GEMINI_API_KEY,
    cdpApiKeyName=CDP_API_KEY_NAME,
    cdpApiKeyPrivateKey=CDP_API_KEY_PRIVATE_KEY,
    networkId=NETWORK_ID,
    sqliteDbPath="./data/checkpoints.sqlite",
)

class Message(BaseModel):
    content: str
    isUser: bool

class ChatHistory(BaseModel):
    messages: list[Message]
    userId: str

class ChatRequest(BaseModel):
    content: str

class ChatResponse(BaseModel):
    message: Message

class AuthToken(BaseModel):
    message: str
    signature: str

w3 = Web3()

def verify_auth_token(authorizationHeader: str | None, userId: str) -> None:
    if authorizationHeader is None:
        raise UnauthorizedException()
    try:
        authTokenJson = base64.b64decode(authorizationHeader).decode('utf-8')
        authToken = AuthToken.model_validate_json(authTokenJson)
        messageHash = encode_defunct(text=authToken.message)
        signerId = w3.eth.account.recover_message(messageHash, signature=authToken.signature)
    except Exception as exception:
        print(f"Signature verification failed: {exception}")
        raise UnauthorizedException()
    if signerId.lower() != userId.lower():
        raise UnauthorizedException()


@app.post("/chats/{userId}/messages", response_model=ChatResponse)
async def create_chat_message(userId: str, request: ChatRequest, authorization: Annotated[str | None, Header()] = None):
    verify_auth_token(authorizationHeader=authorization, userId=userId)
    userMessage = Message(content=request.content, isUser=True)
    agentResponse = await agentManager.get_agent_response(userId=userId, message=userMessage.content)
    agentMessage = Message(content=agentResponse, isUser=False)
    return ChatResponse(message=agentMessage)


@app.get("/chats/{userId}/history", response_model=ChatHistory)
async def get_chat_history(userId: str, authorization: Annotated[str | None, Header()] = None):
    verify_auth_token(authorizationHeader=authorization, userId=userId)
    messages = await agentManager.get_chat_history(userId=userId)
    return ChatHistory(
        userId=userId,
        messages=[Message.model_validate(message) for message in messages],
    )
