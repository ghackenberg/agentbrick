from typing import List, NotRequired, TypedDict


class ModelComponent(TypedDict):
    name: str
    abbreviation: str
    description: str


class ModelInterface(TypedDict):
    component1: str
    component2: str
    description: str


class MainWorkflowState(TypedDict):
    prompt: str
    description: NotRequired[str]
    components: NotRequired[List[ModelComponent]]
    interfaces: NotRequired[List[ModelInterface]]
