from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Union

from .template import PlainText, TemplatePart, Variable


@dataclass(frozen=True)
class Unique:
    value: str
    id: int

    def to_template(self) -> TemplatePart:
        return Variable(self.id)

    def is_unique(self) -> Literal[True]:
        return True

    def to_string(self) -> str:
        return self.value


@dataclass(frozen=True)
class Match:
    value: str

    def to_template(self) -> TemplatePart:
        return PlainText(self.value)

    def is_unique(self) -> Literal[False]:
        return False

    def to_string(self) -> str:
        return self.value


Block = Union[Unique, Match]
