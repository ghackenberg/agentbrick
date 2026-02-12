from pydantic import BaseModel, Field
from typing import List


class Component(BaseModel):
    """Component of the LEGO model."""

    name: str = Field(description="Name of the component.")
    width: float = Field(description="Width of the component in LEGO units.")
    height: float = Field(description="Height of the component in LEGO units.")
    length: float = Field(description="Length of the component in LEGO units.")


class ComponentList(BaseModel):
    """Decomposition of the LEGO model into components."""

    components: List[Component] = Field(description="List of components.")
