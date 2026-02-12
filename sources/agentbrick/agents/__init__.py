from langchain.agents import create_agent

from agentbrick.agents.middlewares import log_model_call, log_tool_call
from agentbrick.models import llama3_2_1b, llama3_2_3b

middlewares = [log_model_call, log_tool_call]

# Generate Description Agent

generate_description_agent = create_agent(
    llama3_2_3b,
    middleware=middlewares,
    system_prompt="You take a user input and derive a detailed description of a realistic LEGO model. Make sure, that the description of the LEGO model is complete and accurate!",
)

# Extract Components Agent

extract_components_agent = create_agent(
    llama3_2_3b,
    middleware=middlewares,
    system_prompt="You take a detailed description of a LEGO model and extract a COMPLETE list of top-level components (i.e. logical groups of bricks) from which the ENTIRE LEGO model can be assembled. For each component, you output one line with the following pattern: '[Unique and concise component name] - [Brief component description]'. You do NOT output ANY additional text!",
)

# Extract Interfaces Agent

extract_interfaces_agent = create_agent(
    llama3_2_3b,
    middleware=middlewares,
    system_prompt="You take a detailed description of a LEGO model and a list of top-level components and extract the interfaces between the components. An interface is a shared surface between two components where they connect. For each interface, you output one line with the following pattern: '[Component name 1] <-> [Component name 2] : [Brief description of the interface]'. You do NOT output ANY additional text!",
)

# Other Agents ...
