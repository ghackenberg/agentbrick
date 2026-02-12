from logging import basicConfig, INFO, getLogger
from sys import argv

from agentbrick.workflows import main_workflow

basicConfig(level=INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = getLogger(__name__)

# Invoke agent

main_workflow.invoke(
    {
        "prompt": argv[1] if len(argv) > 1 else "House",
        "architecture_description": None,
        "architecture_top_level_component_names": None,
    }
)
