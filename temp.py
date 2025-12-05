from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_agent

from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
from langchain_mcp_adapters.tools import load_mcp_tools
from services.utils import split_qwen_output

from models.UserInformation import UserInformation
from models.ChatHistory import ChatHistory

from fastmcp import Client
from datetime import datetime
import asyncio
import warnings

async def supply_chain_response(user_info: UserInformation, history: list[ChatHistory], question: str):
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

    prompt_str = """
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

            Tools to use:
            - get_product_info: اطلاعات محصولات
            اطلاعات تامین کنندگان: search_suppliers
    """

    # model = ChatOllama(
    #     #model="mshojaei77/gemma3persian:latest",
    #     model = "qwen3:8b",
    #     temperature=0.3
    # )

    model = ChatOllama(
        model="qwen3:8b",
        base_url="http://localhost:11434",
    )

    chain = RunnableSequence(
        prompt,
        model,
        StrOutputParser()
    )

    try:
        async with streamablehttp_client("http://localhost:9090/mcp") as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await load_mcp_tools(session)
                agent = create_agent(model, tools, system_prompt=prompt_str)
                response = await agent.ainvoke({"messages": question})
                return split_qwen_output(response["messages"][-1].content)

                print(response)
    except Exception as e:
        print(e)

    # async with Client("mcp_server.py") as client:
    #     call_server = await client.call_tool(
    #         "search_suppliers",
    #         {
    #             "query": question
    #         }
    #     )
    #     context = call_server.content[0].text
    #     response = chain.invoke({
    #         "user_info": user_info,
    #         "history": history,
    #         "context": context,
    #         "question": question
    #     })

    #     return response
