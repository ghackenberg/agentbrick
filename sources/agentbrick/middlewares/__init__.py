from langchain.messages import ToolMessage
from langchain.agents.middleware import (
    ModelRequest,
    ModelResponse,
    ToolCallRequest,
    wrap_model_call,
    wrap_tool_call,
)
from langgraph.types import Command
from logging import getLogger
from typing import Callable

logger = getLogger(__name__)


@wrap_model_call
def log_model_call(
    request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    logger.debug(f"Model call: {request.messages[-1].content}")
    return handler(request)


@wrap_tool_call
def log_tool_call(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command:
    logger.debug(f"Tool call: {request.tool_call['name']}({request.tool_call['args']})")
    return handler(request)
