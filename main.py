from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, ModelResponse, wrap_model_call, wrap_tool_call
from langchain.messages import HumanMessage, SystemMessage
from langchain.tools import tool
from pydantic import BaseModel, Field
from typing import Callable, List

# Initialize LLM

print("Initializing LLM")

llm = ChatOllama(model="llama3.2:1b")

# Define middleware

print("Defining middleware")

@wrap_model_call
def log_model_call(request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
    print("Model call")
    return handler(request)

@wrap_tool_call
def log_tool_call(request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
    print("Tool call")
    return handler(request)

middleware = [log_model_call, log_tool_call]

# Define tools

print("Defining tools")

@tool
def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two numbers.
    
    Args:
        a(int): First number.
        b(int): Second number.
    """
    return a + b

tools = [calculate_sum]

# Define response format

print("Defining response format")

class Component(BaseModel):
    """Component of the LEGO model"""
    name: str = Field(description="Name of the component")
    description: str = Field(description="Description of the component")
    width: int = Field(description="Width of the component in LEGO units")
    height: int = Field(description="Height of the component in LEGO units")
    length: int = Field(description="Length of the component in LEGO units")

class ComponentList(BaseModel):
    """Result of decomposing the LEGO model into components"""
    components: List[Component] = Field(description="The list of components")

response_format = ComponentList

# Define system prompt

print("Defining system prompt")

system_prompt = "You are a digital LEGO modeling agent. You help me divide my model into components."

# Create agent

print("Creating agent")

agent = create_agent(llm, middleware=middleware, tools=tools, response_format=response_format, system_prompt=system_prompt)

# Invoke agent

print("Invoking agent")

answer = agent.invoke({ "messages": [HumanMessage("I want to build a house.")] })

for message in answer["messages"]:
    print(message.content)