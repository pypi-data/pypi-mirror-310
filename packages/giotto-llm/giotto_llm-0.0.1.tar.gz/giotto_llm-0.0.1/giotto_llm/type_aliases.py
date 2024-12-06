from typing import Any, Literal, TypeAlias

Grid: TypeAlias = list[list[int]]
InputOutputPair: TypeAlias = dict[str, Grid]
JSONTask: TypeAlias = dict[str, list[InputOutputPair]]
Attempts: TypeAlias = dict[int, list[Grid]]

Messages: TypeAlias = list[dict[str, str]]
OAIMessage: TypeAlias = list[dict[str, Any]]
