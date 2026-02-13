from logging import getLogger
from matplotlib.pyplot import figure, show
from networkx import draw, Graph
from numpy import zeros
from random import randint
from typing import List

from agentbrick.workflows.states import (
    MainWorkflowState,
    ModelComponent,
    ModelLayer,
    ModelInterface,
)

logger = getLogger(__name__)


def parse_components(content: str) -> List[ModelComponent]:
    components = []
    for line in content.splitlines():
        try:
            if line.strip():
                name, description = line.split(" - ", 1)
                components.append(
                    {
                        "name": name.strip(),
                        "description": description.strip(),
                    }
                )
                logger.info(f"Component: {name.strip()} - {description.strip()}")
            else:
                logger.warning(f"Skipping empty line: {line}")
        except ValueError as e:
            logger.error(f"Error parsing line: {line}. Error: {e}")
    return components


def parse_interfaces(content: str) -> List[ModelInterface]:
    interfaces = []
    for line in content.splitlines():
        try:
            if line.strip():
                components, description = line.split(" : ", 1)
                component1, component2 = components.split(" <-> ")
                interfaces.append(
                    {
                        "component1": component1.strip(),
                        "component2": component2.strip(),
                        "description": description.strip(),
                    }
                )
                logger.info(f"Interface: {component1} <-> {component2} : {description}")
            else:
                logger.warning(f"Skipping empty line: {line}")
        except ValueError as e:
            logger.error(f"Error parsing line: {line}. Error: {e}")
    return interfaces


def visualize_components_and_interfaces(state: MainWorkflowState) -> None:

    graph = Graph()

    for component in state.get("components", []):
        graph.add_node(component["name"], description=component["description"])

    for interface in state.get("interfaces", []):
        graph.add_edge(
            interface["component1"],
            interface["component2"],
            description=interface["description"],
        )

    labels = {
        component["name"]: component["name"]
        for component in state.get("components", [])
    }

    figure(figsize=(12, 8))

    draw(graph, labels=labels)

    show()


COLORS = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'orange', 'purple', 'brown', 'pink']


def visualize_grid_configuration(state: MainWorkflowState) -> None:

    colors: dict[str, str] = {}

    voxels = zeros((state.get("size_x", 0), state.get("size_y", 0), state.get("size_z", 0)), dtype=bool)

    for layer in state.get("layers", []):
        z = layer["z"]
        for row in layer["rows"]:
            y = row["y"]
            for x, cell in enumerate(row["cells"]):
                if cell != "EMPTY":
                    voxels[x, y, z] = True
    
    facecolors = zeros((state.get("size_x", 0), state.get("size_y", 0), state.get("size_z", 0)), dtype=str)

    for layer in state.get("layers", []):
        z = layer["z"]
        for row in layer["rows"]:
            y = row["y"]
            for x, cell in enumerate(row["cells"]):
                if cell != "EMPTY":
                    if cell not in colors:
                        colors[cell] = COLORS[len(colors) % len(COLORS)]
                    facecolors[x, y, z] = colors[cell]

    ax = figure().add_subplot(projection="3d")
    ax.voxels(voxels, facecolors=facecolors, edgecolor="gray")

    show()
