from fastapi import FastAPI
from models.ChatRequest import ChatRequest
from models.UserInformation import UserInformation
from services.sql_server_services import get_user_by_mobile, get_last_chat_history
from temp import supply_chain_response

import uvicorn

app = FastAPI()

@app.post("/chat")
async def chat(request: ChatRequest):
    print(request)
    # userEntity = get_user_by_mobile(request.user.mobile)
    # history = get_last_chat_history(userEntity.user_id, request.platform, limit=5)


    user_info = "نام کاربر: علی، مدیر خرید"
    history = "جلسه قبلی درباره تأمین‌کنندگان برنج بود."
    question = "سلام، برنج فروشی های فردیس رو بهم معرفی می کنی؟"

    response = await supply_chain_response(user_info, history, question)

    return {
        "status": "ok",
        "response": response
    }
    # return {
    #     "status": "ok",
    #     "prompt": request.prompt,
    #     "user": userEntity,
    #     "history": history
    # }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=1010,
        reload=True
    )