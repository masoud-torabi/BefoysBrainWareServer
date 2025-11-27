import os
import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama import ChatOllama

app = FastAPI()

ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")

llm = ChatOllama(
    model="mshojaei77/gemma3persian:latest",
    base_url=ollama_host,
    temperature=0
)


class AskRequest(BaseModel):
    prompt: str


@app.post("/ask")
def ask_llm(request: AskRequest):
    response = llm.invoke(request.prompt)
    return {"response": response}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
