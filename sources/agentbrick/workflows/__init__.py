from langchain.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from logging import getLogger

from agentbrick.agents import architecture_description_agent, architecture_model_agent
from agentbrick.agents.responses import ArchitectureModelAgentResponse
from agentbrick.workflows.states import MainWorkflowState

logger = getLogger(__name__)


def call_architecture_description_agent(state: MainWorkflowState) -> MainWorkflowState:
    answer = architecture_description_agent.invoke(
        {"messages": [HumanMessage(state["prompt"])]}
    )
    state["architecture_description"] = answer["messages"][-1].content
    return state

def call_architecture_model_agent(state: MainWorkflowState) -> MainWorkflowState:
    answer = architecture_model_agent.invoke(
        {"messages": [HumanMessage(state["architecture_description"])]}
    )
    state["architecture_top_level_component_names"] = answer["messages"][-1].content.splitlines()
    for component in state["architecture_top_level_component_names"]:
        logger.info(f"Identified component: {component}")
    return state


main_workflow_graph = StateGraph(MainWorkflowState)
main_workflow_graph.add_node("architecture_description_agent", call_architecture_description_agent)
main_workflow_graph.add_node("architecture_model_agent", call_architecture_model_agent)
main_workflow_graph.add_edge(START, "architecture_description_agent")
main_workflow_graph.add_edge("architecture_description_agent", "architecture_model_agent")
main_workflow_graph.add_edge("architecture_model_agent", END)

main_workflow = main_workflow_graph.compile()
