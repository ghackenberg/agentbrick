from langchain.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from logging import getLogger

from agentbrick.agents import (
    generate_description_agent,
    extract_components_agent,
    extract_interfaces_agent,
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
                    name, description = line.split(" - ", 1)
                    state["components"].append(
                        {
                            "name": name.strip(),
                            "description": description.strip(),
                        }
                    )
                    logger.info(f"Component: {name} - {description}")
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


main_workflow_graph = StateGraph(MainWorkflowState)

main_workflow_graph.add_node("generate_description", generate_description)
main_workflow_graph.add_node("extract_components", extract_components)
main_workflow_graph.add_node("extract_interfaces", extract_interfaces)

main_workflow_graph.add_edge(START, "generate_description")
main_workflow_graph.add_edge("generate_description", "extract_components")
main_workflow_graph.add_edge("extract_components", "extract_interfaces")
main_workflow_graph.add_edge("extract_interfaces", END)

main_workflow = main_workflow_graph.compile()
