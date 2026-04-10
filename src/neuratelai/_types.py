from __future__ import annotations

from typing import Any, TypeAlias


class _NotGiven:
    """Sentinel for parameters not explicitly provided (distinct from None)."""

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "NOT_GIVEN"


NOT_GIVEN = _NotGiven()
NotGiven: TypeAlias = _NotGiven

QueryParamValue: TypeAlias = str | int | float | bool | None
QueryParams: TypeAlias = dict[str, QueryParamValue | list[QueryParamValue]]
JSON: TypeAlias = Any
Headers: TypeAlias = dict[str, str]
