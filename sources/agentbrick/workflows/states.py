from typing import List, NotRequired, TypedDict


class ModelComponent(TypedDict):
    name: str
    description: str


class ModelInterface(TypedDict):
    component1: str
    component2: str
    description: str


class ModelRow(TypedDict):
    cells: List[str]


class ModelLayer(TypedDict):
    rows: List[ModelRow]


class MainWorkflowState(TypedDict):
    prompt: str

    size_x: int
    size_y: int
    size_z: int

    description: NotRequired[str]

    components: NotRequired[List[ModelComponent]]

    interfaces: NotRequired[List[ModelInterface]]

    next_x: NotRequired[int]
    next_y: NotRequired[int]
    next_z: NotRequired[int]

    layers: NotRequired[List[ModelLayer]]
