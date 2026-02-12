from typing import TypedDict

from agentbrick.agents.responses import ArchitectureModelNode


class MainWorkflowState(TypedDict):
    prompt: str
    architecture_description: str
    architecture_model: ArchitectureModelNode
