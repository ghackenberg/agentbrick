from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

from agentbrick.agents.middlewares import log_model_call, log_tool_call
from agentbrick.agents.responses import ArchitectureModelAgentResponse
from agentbrick.models import llama3_2_3b

middlewares = [log_model_call, log_tool_call]

# Generate Description Agent

generate_description_agent = create_agent(
    llama3_2_3b,
    middleware=middlewares,
    system_prompt="You take a user input and generate a detailed description of the LEGO model.",
)

# Extract Components Agent

extract_components_agent = create_agent(
    llama3_2_3b,
    middleware=middlewares,
    system_prompt="You take a detailed description of a LEGO model and extract a COMPLETE list of top-level components (i.e. logical groups of bricks) from which the ENTIRE LEGO model can be assembled. For each component, you output one line with the following pattern: '[Unique and concise component name] - [Brief component description]'. You do NOT output ANY additional text!",
)

# Other Agents ...
