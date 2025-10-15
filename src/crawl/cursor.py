"""
A decorator/handler for cursors in API calls.
"""

from functools import wraps
from typing import Callable, Generic, ParamSpec, TypeGuard, TypeVar

from pydantic import BaseModel
from sirene3 import Header

T = TypeVar("T", bound=BaseModel)
P = ParamSpec("P")


class ResponseHasHeaders(Generic[T]):
    header: Header


def _have_results_and_header(
    results: T,
) -> TypeGuard[ResponseHasHeaders[T]]:
    return results is not None and getattr(results, "header") is not None


class ApiCursor:
    def __init__(self):
        self.cursor = "*"

    def use(
        self, fn: Callable[P, T]
    ) -> Callable[P, ResponseHasHeaders[T] | None]:
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs):
            kwargs["curseur"] = self.cursor
            results = fn(*args, **kwargs)

            if not _have_results_and_header(results):
                return None
            self.cursor = results.header.curseur_suivant
            return results

        return wrapper
