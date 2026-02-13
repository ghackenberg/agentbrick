from langchain.messages import AIMessage, HumanMessage
from logging import getLogger

from agentbrick.agents import (
    generate_description_agent,
    extract_components_agent,
    extract_interfaces_agent,
    define_cells_agent,
)
from agentbrick.workflows.states import MainWorkflowState
from agentbrick.workflows.helpers import (
    parse_components,
    parse_interfaces,
    visualize_components_and_interfaces,
    visualize_grid_configuration,
)

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
            state["components"] = parse_components(content)
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
                            f"{c['name']} - {c['description']}"
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
            state["interfaces"] = parse_interfaces(content)
            visualize_components_and_interfaces(state)
        else:
            logger.warning(f"Unexpected content type: {type(content)}")
    else:
        logger.warning(f"Unexpected message type: {type(message)}")
    return state


def define_cells(state: MainWorkflowState) -> MainWorkflowState:
    layers = state.get("layers", [])

    next_x = state.get("next_x", 0)
    next_y = state.get("next_y", 0)
    next_z = state.get("next_z", 0)

    answer = define_cells_agent.invoke(
        {
            "messages": [
                HumanMessage(
                    "DESCRIPTION:\n"
                    + state.get("description", "")
                    + "\n\n---\n\nCOMPONENTS:\n"
                    + "\n".join(
                        [
                            f"{c['name']} - {c['description']}"
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
                    + "\n\n---\n\nGRID SIZE:\n"
                    + f"x={state['size_x']}, y={state['size_y']}, z={state['size_z']}"
                    + "\n\n---\n\nNEXT CELL:\n"
                    + f"x={next_x}, y={next_y}, z={next_z}"
                    + "\n\n---\n\nCURRENT GRID CONFIGURATION:\n"
                    + "\n".join(
                        (
                            f"z={z}:\n"
                            + "\n".join(
                                [
                                    f"y={y}: " + "; ".join(r["cells"])
                                    for y, r in enumerate(l["rows"])
                                ]
                            )
                            for z, l in enumerate(layers)
                        )
                        if layers
                        else "None"
                    )
                )
            ]
        }
    )
    message = answer["messages"][-1]
    if isinstance(message, AIMessage):
        content = message.content
        if isinstance(content, str):
            logger.info(f"Cell x={next_x}, y={next_y}, z={next_z}: {content}")
            if next_z == 0:
                layers.append({"rows": []})
            if next_y == 0:
                layers[next_z]["rows"].append({"cells": []})
            layers[next_z]["rows"][next_y]["cells"].append(content)
            state["layers"] = layers
            state["next_x"] = (next_x + 1) % state["size_x"]
            state["next_y"] = (
                (next_y + 1) % state["size_y"] if state["next_x"] == 0 else next_y
            )
            state["next_z"] = (
                next_z + 1 if state["next_y"] == 0 and state["next_x"] == 0 else next_z
            )
            if state["next_x"] == 0 and state["next_y"] == 0:
                visualize_grid_configuration(state)
        else:
            logger.warning(f"Unexpected content type: {type(content)}")
    else:
        logger.warning(f"Unexpected message type: {type(message)}")
    return state
