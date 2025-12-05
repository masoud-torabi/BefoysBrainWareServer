from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.ChatRequest import ChatRequest
from models.UserInformation import UserInformation
from services.sql_server_services import *
from temp import supply_chain_response

import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: ChatRequest):
    
    userEntity = get_user_by_mobile(request.user.mobile)
    history = get_last_chat_history(userEntity.user_id, request.platform, limit=5)

    response = await supply_chain_response(userEntity, history, request.prompt)

    insert_chat_message(
        chat_id=None,
        type="text",
        message=request.prompt,
        response_message=response,
        response_type="text",
    )

    return {
        "status": "ok",
        "prompt": request.prompt,
        "response": response,
        "user": userEntity,
        "history": history
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=1010,
        reload=True
    )