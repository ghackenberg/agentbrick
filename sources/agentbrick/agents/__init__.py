from langchain.agents import create_agent

from agentbrick.agents.middlewares import log_model_call, log_tool_call
from agentbrick.models import llama3_2_3b

middlewares = [log_model_call, log_tool_call]

# Generate Description Agent

generate_description_agent = create_agent(
    llama3_2_3b,
    middleware=middlewares,
    system_prompt=(
        "You take a user input and derive a detailed description of a realistic LEGO model."
        " Make sure, that the description of the LEGO model is complete and accurate!"
    ),
)

# Extract Components Agent

extract_components_agent = create_agent(
    llama3_2_3b,
    middleware=middlewares,
    system_prompt=(
        "You take a detailed description of a LEGO model and extract a COMPLETE list of top-level components (i.e. logical groups of bricks) from which the ENTIRE LEGO model can be assembled."
        " For each component, you output one line with the following pattern: '[Unique and concise component name] - [Brief component description]'."
        " You do NOT output ANY additional text!"
    ),
)

# Extract Interfaces Agent

extract_interfaces_agent = create_agent(
    llama3_2_3b,
    middleware=middlewares,
    system_prompt=(
        "You take a detailed description of a LEGO model and a list of top-level components and extract the interfaces between the components."
        " An interface is a shared surface between two components where they connect."
        " For each interface, you output one line with the following pattern: '[Component name 1] <-> [Component name 2] : [Brief description of the interface]'."
        " You do NOT output ANY additional text!"
    ),
)

# Generate Grid Configuration Agent

generate_grid_configuration_agent = create_agent(
    llama3_2_3b,
    middleware=middlewares,
    system_prompt=(
        "You take a detailed description of a LEGO model, a list of top-level components, a list of interfaces between the components, and output a 3D grid configuration."
        " You describe the 3D grid configuration layer by layer starting at the bottom layer (z=0) and ending at the top layer (z=10 MANDATORY)."
        " In the output, you start each 2D layer with a line 'Layer z=[z-value]:' followed by the 2D layer configuration."
        " You describe the 2D layer configuration row by row starting at the front row (y=0) and ending at the back row (y=10 MANDATORY)."
        " In the output, you start each row with a line 'Row y=[y-value]:' followed by the 2D row configuration."
        " You describe the 2D row configuration in one line, cell by cell separated by semi-colons, starting at the leftmost cell (x=0) and ending at the rightmost cell (x=10 MANDATORY)."
        " In the output, you represent each cell with the number of the component that occupies the cell or '0' if the cell is empty."
        " You do NOT output ANY additional text!"
    ),
)

# Other Agents ...
