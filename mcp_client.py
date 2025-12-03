from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser

from fastmcp import Client
from datetime import datetime
import asyncio
import warnings

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
warnings.filterwarnings("ignore", category=ResourceWarning)

model = ChatOllama(
    model="mshojaei77/gemma3persian:latest",
    temperature=0.3
)

async def main():

    print("started at ", datetime.now())
    user_info = """
    - نام کاربر: مسعود
    - نقش: مدیر انبار
    - سطح دسترسی: کامل
    - زبان ترجیحی: فارسی
    """

    chat_history = """
    User: چرا تامین‌کننده بهار دشت در تحویل تخم‌مرغ تأخیر دارد؟
    Assistant: معمولاً این تأخیرها به علت مشکلات حمل‌ونقل یا ظرفیت تولید ایجاد می‌شود.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        Role:\n
        You are a polite and professional Supply Chain Manager working in the hospitality industry (hotels and restaurants). 
            Your job is to answer users’ questions about supply chain processes, procurement, inventory management, logistics, 
            and supplier coordination.

            Guidelines:
            - Always answer briefly and clearly.
            - Be polite and use professional tone.
            - Focus on practical, business-oriented advice.
            - Avoid long explanations or unnecessary details.
            - If a question is unclear, ask politely for clarification.
            - Never use slang or informal language.
            - Respond in Persian unless the user explicitly uses another language.
            - Your Software developer is 'befoys technology team'
            - Use user's info in some of responds

            Example style:
            User: How can we reduce delivery delays?
            Assistant: Certainly. You can reduce delays by improving supplier scheduling and monitoring transport performance weekly.

        """),
        ("system", "User Information:\n{user_info}"),
        ("system", "Chat History:\n{history}"),
        ("system", "Context:\n{context}"),

        ("human", "{question}")
    ])

    chain = RunnableSequence(
        prompt,
        model,
        StrOutputParser()
    )
    
    user_question = "سلام، برنج فروشی های فردیس رو بهم معرفی می کنی؟"

    async with Client("mcp_server.py") as client:
        call_server = await client.call_tool(
            "search_suppliers",
            {
                "query": user_question
            }
        )
        
        context = call_server.content[0].text

        response = chain.invoke({
            "user_info": user_info,
            "history": chat_history,
            "context": context,
            "question": user_question
        })

        print(response)
        print("finished at ", datetime.now())        



if __name__ == "__main__":
    asyncio.run(main())