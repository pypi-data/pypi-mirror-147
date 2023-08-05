import builtins
import inspect
from typing import Any, Callable

from functon.types import FunctonFunction


def defun(body: tuple) -> Callable:
    """Runs functions and returns results."""

    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])

    frame_context = frame.code_context[0]
    function_name = frame_context[4 : frame_context.find("(")]

    return FunctonFunction(func_name=function_name, func_code=body, func_module=module)


def fn(func: Callable, *args: Any) -> Any:
    """Run function and return result."""

    if hasattr(builtins, func.__name__):
        return func(*args)
    return func.__annotations__["return"](args)
