from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser

from models.UserInformation import UserInformation
from models.ChatHistory import ChatHistory

from fastmcp import Client
from datetime import datetime
import asyncio
import warnings

async def make_response(user_info: UserInformation, history: list[ChatHistory], question: str):
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
            - Your Software developer is 'تیم تکنولوژی بیفویز'
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

    model = ChatOllama(
        model="mshojaei77/gemma3persian:latest",
        temperature=0.3
    )

    chain = RunnableSequence(
        prompt,
        model,
        StrOutputParser()
    )

    # Query MCP server for supplier info
    async with Client("mcp_server.py") as client:
        call_server = await client.call_tool(
            "search_suppliers",
            {
                "query": question
            }
        )
        context = call_server.content[0].text

        print("Context: \n", context)

        # Run the chain with all inputs
        response = chain.invoke({
            "user_info": user_info,
            "history": history,
            "context": context,
            "question": question
        })

        return response
