from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from logging import getLogger

from agentbrick.agents.responses import ArchitectureModelAgentResponse
from agentbrick.models import llama3_2_3b

logger = getLogger(__name__)



# Architecture Description Agent

architecture_description_agent = create_agent(
    llama3_2_3b,
    system_prompt="You are an archtecture description agent. You take a natural language description of something, the user wants to build, and you output a structured description of the architecture of that thing.",
)

# Architecture Model Agent

architecture_model_agent = create_agent(
    llama3_2_3b,
    system_prompt="You are an architecture model agent. You take a structured description of the architecture of something, and you output a structured description of the components needed to build that thing.",
    response_format=ToolStrategy(ArchitectureModelAgentResponse)
)

# Other Agents ...
