# **AgentBrick** - From Chat to CAD

![AgentBrick Logo](assets/preview.jpg)

**AgentBrick** is an open-source framework designed to bridge the gap between natural language and the **LDraw** standard. By leveraging **LangChain agents** and **LangGraph workflows**, AgentBrick transforms user prompts into valid, structured LDraw models, allowing for iterative refinement through conversational AI.

## Project structure

- [assets/](./assets/) - Project assets (icon, logo, social preview image, ...)
- [sources/](./sources/) - Source code
  - [agentbrick/](./sources/agentbrick/) - AgentBrick library
    - [models/](./sources/agentbrick/models/) - Language models (e.g. llama 3.2)
    - [agents/](./sources/agentbrick/agents/) - Agent definitions
      - [middlewares/](./sources/agentbrick/middlewares/) - Middleware (log model call, log tool call, ...)
      - [responses/](./sources/agentbrick/responses/) - Response formats (i.e. pydantic schema classes)
      - [tools/](./sources/agentbrick/tools/) - Tools
    - [workflows/](./sources/agentbrick/workflows/) - Workflow definitions
      - [states/](./sources/agentbrick/states/) - State definitions
  - [main.py](./sources/main.py) - Main program
- [requirements.txt](./requirements.txt) - Project dependencies

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