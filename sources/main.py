from logging import basicConfig, getLogger, INFO, ERROR
from sys import argv

from agentbrick.workflows import main_workflow

basicConfig(level=INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

getLogger("httpx").setLevel(ERROR)

# Invoke agent

main_workflow.invoke(
    {
        "prompt": argv[1] if len(argv) > 1 else "House",
        "size_x": 5,
        "size_y": 5,
        "size_z": 5,
    }
)
