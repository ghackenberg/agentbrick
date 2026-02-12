from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

from agentbrick.agents.middlewares import log_model_call, log_tool_call
from agentbrick.agents.responses import ArchitectureModelAgentResponse
from agentbrick.models import llama3_2_3b

middlewares = [log_model_call, log_tool_call]

# Architecture Description Agent

architecture_description_agent = create_agent(
    llama3_2_3b,
    middleware=middlewares,
    system_prompt="You take a user input and generate a detailed description of the LEGO model.",
)

# Architecture Model Agent

architecture_model_agent = create_agent(
    llama3_2_3b,
    middleware=middlewares,
    system_prompt="You take a detailed description of a LEGO model and extract a complete list of top-level logical component names (no bricks). You only output the component names separated by line breaks. You do NOT output additional text!",
)

# Other Agents ...
