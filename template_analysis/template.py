from __future__ import annotations

from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Variable:
    id: int

    def to_format_string(self) -> str:
        return "{}"


@dataclass(frozen=True)
class PlainText:
    value: str

    def to_format_string(self) -> str:
        return self.value


TemplatePart = Union[PlainText, Variable]


@dataclass
class Template:
    parts: list[TemplatePart]

    def to_format_string(self) -> str:
        return "".join(part.to_format_string() for part in self.parts)
