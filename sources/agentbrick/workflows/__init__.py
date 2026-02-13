from langgraph.graph import END, START, StateGraph
from logging import getLogger

from agentbrick.workflows.nodes import (
    generate_description,
    extract_components,
    extract_interfaces,
    generate_grid_configuration,
)
from agentbrick.workflows.states import MainWorkflowState

logger = getLogger(__name__)


main_workflow_graph = StateGraph(MainWorkflowState)

main_workflow_graph.add_node("generate_description", generate_description)
main_workflow_graph.add_node("extract_components", extract_components)
main_workflow_graph.add_node("extract_interfaces", extract_interfaces)
main_workflow_graph.add_node("generate_grid_configuration", generate_grid_configuration)

main_workflow_graph.add_edge(START, "generate_description")
main_workflow_graph.add_edge("generate_description", "extract_components")
main_workflow_graph.add_edge("extract_components", "extract_interfaces")
main_workflow_graph.add_edge("extract_interfaces", "generate_grid_configuration")
main_workflow_graph.add_edge("generate_grid_configuration", END)

main_workflow = main_workflow_graph.compile()
