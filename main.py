from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, ModelResponse, wrap_model_call, wrap_tool_call
from langchain.agents.structured_output import ToolStrategy
from langchain.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain.tools import tool
from logging import basicConfig, INFO, getLogger
from pydantic import BaseModel, Field
from sys import argv
from typing import Callable, List

basicConfig(level=INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = getLogger(__name__)

# Initialize LLM

logger.debug("Initializing LLM")

llm = ChatOllama(model="llama3.2:3b")

# Define middleware

logger.debug("Defining middleware")

@wrap_model_call
def log_model_call(request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
    logger.debug("Model call")
    return handler(request)

@wrap_tool_call
def log_tool_call(request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
    logger.debug("Tool call")
    return handler(request)

middleware = [log_model_call, log_tool_call]

# Define tools

logger.debug("Defining tools")

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

logger.debug("Defining response format")

class Component(BaseModel):
    """Component of the LEGO model."""
    name: str = Field(description="Name of the component.")
    width: float = Field(description="Width of the component in LEGO units.")
    height: float = Field(description="Height of the component in LEGO units.")
    length: float = Field(description="Length of the component in LEGO units.")

class ComponentList(BaseModel):
    """Decomposition of the LEGO model into components."""
    components: List[Component] = Field(description="List of components.")

response_format = ToolStrategy(ComponentList)

# Define system prompt

logger.debug("Defining system prompt")

system_prompt = "Divide the LEGO model into components."

# Create agent

logger.debug("Creating agent")

agent = create_agent(llm, middleware=middleware, tools=tools, system_prompt=system_prompt, response_format=response_format)

# Invoke agent

logger.debug("Invoking agent")

answer = agent.invoke({ "messages": [HumanMessage(argv[1])] })

if "structured_response" in answer:
    structured_response = answer["structured_response"]
    if isinstance(structured_response, ComponentList):
        for component in structured_response.components:
            logger.info(f"Component: {component.name}, Width: {component.width}, Height: {component.height}, Length: {component.length}")
    else:
        logger.warning(f"Unexpected structured response type: {type(structured_response)}")
else:
    logger.warning("No structured response found.")