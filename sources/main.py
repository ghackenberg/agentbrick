from logging import basicConfig, INFO, getLogger

from agentbrick.workflows import main_workflow

basicConfig(level=INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = getLogger(__name__)

# Invoke agent

main_workflow.invoke({"prompt": "House"})
