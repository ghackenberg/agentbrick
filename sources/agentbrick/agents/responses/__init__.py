from pydantic import BaseModel, Field
from typing import List


class ArchitectureModelNode(BaseModel):
    """Node in the architecture model."""

    name: str = Field(description="Name of the node.")
    children: List["ArchitectureModelNode"] = Field(
        default_factory=list, description="Child nodes in the architecture model."
    )

class ArchitectureModelAgentResponse(BaseModel):
    """Response from the architecture model agent."""

    root: ArchitectureModelNode = Field(description="Root node of the architecture model.")