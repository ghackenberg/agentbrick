from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

from agentbrick.agents.middlewares import log_model_call, log_tool_call
from agentbrick.agents.responses import ComponentList
from agentbrick.agents.tools import calculate_sum
from agentbrick.models import llama3_2_3b

middleware = [log_model_call, log_tool_call]

tools = [calculate_sum]

system_prompt = "Divide the LEGO model into components."

response_format = ToolStrategy(ComponentList)

agent = create_agent(
    llama3_2_3b,
    middleware=middleware,
    tools=tools,
    system_prompt=system_prompt,
    response_format=response_format,
)
