from langchain.messages import HumanMessage
from logging import basicConfig, INFO, getLogger

from agentbrick.agents import agent
from agentbrick.schemas import ComponentList

basicConfig(level=INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = getLogger(__name__)

# Invoke agent

logger.debug("Invoking agent")

answer = agent.invoke(
    {"messages": [HumanMessage("I want to build a LEGO model of a house.")]}
)

if "structured_response" in answer:
    structured_response = answer["structured_response"]
    if isinstance(structured_response, ComponentList):
        for component in structured_response.components:
            logger.info(
                f"Component: {component.name}, Width: {component.width}, Height: {component.height}, Length: {component.length}"
            )
    else:
        logger.warning(
            f"Unexpected structured response type: {type(structured_response)}"
        )
else:
    logger.warning("No structured response found.")
