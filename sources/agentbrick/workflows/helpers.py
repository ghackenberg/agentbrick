from logging import getLogger
from matplotlib.pyplot import figure, show
from networkx import draw, Graph
from typing import List

from agentbrick.workflows.states import (
    MainWorkflowState,
    ModelComponent,
    ModelInterface,
)

logger = getLogger(__name__)


def parse_components(content: str) -> List[ModelComponent]:
    components = []
    for line in content.splitlines():
        if line.strip():
            name_and_abbreviation, description = line.split(" - ", 2)
            name = name_and_abbreviation.rsplit("(", 1)[0].strip()
            abbreviation = name_and_abbreviation.rsplit("(", 1)[1].rstrip(")").strip()
            components.append(
                {
                    "name": name.strip(),
                    "abbreviation": abbreviation.strip(),
                    "description": description.strip(),
                }
            )
            logger.info(f"Component: {name} ({abbreviation}) - {description.strip()}")
        else:
            logger.warning(f"Skipping empty line: {line}")

    return components


def parse_interfaces(content: str) -> List[ModelInterface]:
    interfaces = []
    for line in content.splitlines():
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

    return interfaces


def visualize_components_and_interfaces(state: MainWorkflowState) -> None:

    graph = Graph()

    for component in state.get("components", []):
        graph.add_node(component["abbreviation"], description=component["description"])

    for interface in state.get("interfaces", []):
        graph.add_edge(
            interface["component1"],
            interface["component2"],
            description=interface["description"],
        )

    labels = {
        component["abbreviation"]: component["name"]
        for component in state.get("components", [])
    }

    figure(figsize=(12, 8))

    draw(graph, labels=labels)

    show()
