from collections.abc import Iterable
from typing import Callable

from functon.types import Expr


def RETURN(expr: Expr):
    return expr


def IF(cond: bool, true_expr: Expr, false_expr: Expr) -> Expr:
    if cond:
        return true_expr
    return false_expr


def FOR(it: Iterable, body: Callable | tuple) -> None:
    if isinstance(body, Callable):
        for i in it:
            body(i)
    else:
        for i in it:
            body
