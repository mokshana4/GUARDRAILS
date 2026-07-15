import re
from langchain.tools import tool
from langchain_mistralai import ChatMistralAI
from langchain_classic.agents import (
    create_tool_calling_agent,
    AgentExecutor,
)
from langchain_core.prompts import ChatPromptTemplate

#LLM
llm = ChatMistralAI(
    model="mistral-small-2506",
    temperature = 0
)

#Tool
@tool
def calculator(expression: str) -> str:
    """Evaluates simple mathematical expressions."""

    return str(eval(expression))

#MiddleWare
def pii_middleware(user_input):

    #Hide Email 
    user_input = re.sub(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        "[EMAIL]",
        user_input
    )

    # Hide Phone Number
    user_input = re.sub(
        r"\b\d{10}\b",
        "[PHONE]",
        user_input
    )

    return user_input

prompt = ChatPromptTemplate.from_messages(
    [
        ("system" , "You are a helpful AI assistant"),
        ("Human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ]
)

agent = create_tool_calling_agent(
    llm = llm,
    tools = [calculator],
    prompt = prompt
)

agent_executor = AgentExecutor(
    agent = agent,
    tools = [calculator],
    verbose = True
)

input = """
My email is moskhanahsygy8@gmail.com

My phone number is 8487473390

what is 87+78?
"""

print("Original Input: \n")
print(input)

safe_input = pii_middleware(input)

print("\nAfter Middleware:\n")
print(safe_input)

# -------------------------------
# Agent Executes
# -------------------------------

response = agent_executor.invoke(
    {
        "input": safe_input
    }
)

print("\nFinal Response:\n")
print(response["output"])