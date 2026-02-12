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
    logger.info(f"Model reqest: {request}")
    response = handler(request)
    logger.info(f"Model response: {response}")
    return response


@wrap_tool_call
def log_tool_call(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command:
    logger.info(f"Tool call request: {request.tool_call['name']}({request.tool_call['args']})")
    response = handler(request)
    logger.info(f"Tool call response: {response}")
    return response
