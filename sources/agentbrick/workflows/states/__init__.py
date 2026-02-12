from typing import List, TypedDict


class MainWorkflowState(TypedDict):
    prompt: str
    architecture_description: str | None
    architecture_top_level_component_names: List[str] | None
