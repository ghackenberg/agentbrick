# **AgentBrick** - From Chat to CAD

![AgentBrick Logo](assets/preview.jpg)

**AgentBrick** is an open-source framework designed to bridge the gap between natural language and the **LDraw** standard. By leveraging **LangChain agents** and **LangGraph workflows**, AgentBrick transforms user prompts into valid, structured LDraw models, allowing for iterative refinement through conversational AI.

## Project structure

- [assets/](./assets/) - Project assets (icon, logo, social preview image, ...)
- [sources/](./sources/) - Source code
  - [agentbrick/](./sources/agentbrick/) - AgentBrick library
    - [agents/](./sources/agentbrick/agents/) - Agent package
      - [middlewares.py](./sources/agentbrick/agents/middlewares.py) - Middleware definitions (e.g. `log_model_call`)
      - [responses.py](./sources/agentbrick/agents/responses.py) - Response definitions (i.e. pydantic schema classes)
      - [tools.py](./sources/agentbrick/agents/tools.py) - Tool definitions (e.g. `calculate_sum`)
      - [\_\_init__.py](./sources/agentbrick/agents/__init__.py) - Agent definitions (e.g. `generate_description_agent`)
    - [workflows/](./sources/agentbrick/workflows/) - Workflow package
      - [states.py](./sources/agentbrick/workflows/states.py) - State definitions
      - [\_\_init__.py](./sources/agentbrick/workflows/__init__.py) - Workflow definitions
    - [models.py](./sources/agentbrick/models.py) - Model definitions (e.g. llama 3.2)
  - [main.py](./sources/main.py) - Main program
- [requirements.txt](./requirements.txt) - Project dependencies

## User guide

```python
from agentbrick.workflows import main_workflow

main_workflow.invoke({ "prompt": "House" })
main_workflow.invoke({ "prompt": "Pirate ship" })
main_workflow.invoke({ "prompt": "Princess castle" })
```

## Developer guide

Install dependencies

```sh
pip install -r requirements.txt
```

Linting

```sh
black .
```

Static type checking

```sh
pyright
```