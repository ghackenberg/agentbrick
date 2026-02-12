from pydantic import BaseModel, Field
from typing import List


class ArchitectureModelComponent(BaseModel):
    """Component of the architecture model."""

    name: str = Field(description="Name of the component.")

    description: str = Field(description="Description of the component.")

    width: float = Field(description="Width of the component in LEGO units.")
    height: float = Field(description="Height of the component in LEGO units.")
    length: float = Field(description="Length of the component in LEGO units.")

class ArchitectureModelAgentResponse(BaseModel):
    """Response from the architecture model agent."""

    components: List[ArchitectureModelComponent] = Field(description="List of components in the architecture model.")