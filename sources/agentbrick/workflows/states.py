from typing import List, Optional, TypedDict


class ModelComponent(TypedDict):
    name: str
    description: str


class ModelInterface(TypedDict):
    component1: str
    component2: str
    description: str


class MainWorkflowState(TypedDict):
    prompt: str
    description: str
    components: List[ModelComponent]
    interfaces: List[ModelInterface]
