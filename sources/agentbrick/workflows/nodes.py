from langchain.messages import AIMessage, HumanMessage
from logging import getLogger

from agentbrick.agents import (
    generate_description_agent,
    extract_components_agent,
    extract_interfaces_agent,
    generate_grid_configuration_agent,
)
from agentbrick.workflows.states import MainWorkflowState

logger = getLogger(__name__)


def generate_description(state: MainWorkflowState) -> MainWorkflowState:
    answer = generate_description_agent.invoke(
        {"messages": [HumanMessage(state["prompt"])]}
    )
    state["description"] = answer["messages"][-1].content
    return state


def extract_components(state: MainWorkflowState) -> MainWorkflowState:
    answer = extract_components_agent.invoke(
        {"messages": [HumanMessage(state.get("description", ""))]}
    )
    message = answer["messages"][-1]
    if isinstance(message, AIMessage):
        content = message.content
        if isinstance(content, str):
            state["components"] = []
            for line in content.splitlines():
                if line.strip():
                    name_and_abbreviation, description = line.split(" - ", 2)
                    name = name_and_abbreviation.rsplit("(", 1)[0].strip()
                    abbreviation = (
                        name_and_abbreviation.rsplit("(", 1)[1].rstrip(")").strip()
                    )
                    state["components"].append(
                        {
                            "name": name.strip(),
                            "abbreviation": abbreviation.strip(),
                            "description": description.strip(),
                        }
                    )
                    logger.info(
                        f"Component: {name} ({abbreviation}) - {description.strip()}"
                    )
                else:
                    logger.warning(f"Skipping empty line: {line}")
        else:
            logger.warning(f"Unexpected content type: {type(content)}")
    else:
        logger.warning(f"Unexpected message type: {type(message)}")
    return state


def extract_interfaces(state: MainWorkflowState) -> MainWorkflowState:
    answer = extract_interfaces_agent.invoke(
        {
            "messages": [
                HumanMessage(
                    "DESCRIPTION:\n"
                    + state.get("description", "")
                    + "\n\n---\n\nCOMPONENTS:\n"
                    + "\n".join(
                        [
                            f"{c['name']} ({c['abbreviation']}) - {c['description']}"
                            for c in state.get("components", [])
                        ]
                    )
                )
            ]
        }
    )
    message = answer["messages"][-1]
    if isinstance(message, AIMessage):
        content = message.content
        if isinstance(content, str):
            state["interfaces"] = []
            for line in content.splitlines():
                if line.strip():
                    components, description = line.split(" : ", 1)
                    component1, component2 = components.split(" <-> ")
                    state["interfaces"].append(
                        {
                            "component1": component1.strip(),
                            "component2": component2.strip(),
                            "description": description.strip(),
                        }
                    )
                    logger.info(
                        f"Interface: {component1} <-> {component2} : {description}"
                    )
                else:
                    logger.warning(f"Skipping empty line: {line}")
        else:
            logger.warning(f"Unexpected content type: {type(content)}")
    else:
        logger.warning(f"Unexpected message type: {type(message)}")
    return state


def generate_grid_configuration(state: MainWorkflowState) -> MainWorkflowState:
    answer = generate_grid_configuration_agent.invoke(
        {
            "messages": [
                HumanMessage(
                    "DESCRIPTION:\n"
                    + state.get("description", "")
                    + "\n\n---\n\nCOMPONENTS:\n"
                    + "\n".join(
                        [
                            f"{c['name']} ({c['abbreviation']}) - {c['description']}"
                            for c in state.get("components", [])
                        ]
                    )
                    + "\n\n---\n\nINTERFACES:\n"
                    + "\n".join(
                        [
                            f"{i['component1']} <-> {i['component2']} : {i['description']}"
                            for i in state.get("interfaces", [])
                        ]
                    )
                )
            ]
        }
    )
    message = answer["messages"][-1]
    if isinstance(message, AIMessage):
        content = message.content
        if isinstance(content, str):
            logger.info(f"Grid configuration:\n{content}")
        else:
            logger.warning(f"Unexpected content type: {type(content)}")
    else:
        logger.warning(f"Unexpected message type: {type(message)}")
    return state