from langgraph.graph import END

from agentbrick.workflows.states import MainWorkflowState


def has_more_cells(state: MainWorkflowState) -> str:
    if state.get("next_z", 0) == state["size_z"]:
        return END
    else:
        return "generate_cells"
