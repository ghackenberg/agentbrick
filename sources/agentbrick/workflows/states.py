from typing import List, TypedDict


class ModelComponent(TypedDict):
    name: str
    description: str


class MainWorkflowState(TypedDict):
    prompt: str
    description: str | None
    components: List[ModelComponent] | None
