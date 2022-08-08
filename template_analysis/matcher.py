from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Union

from .symbol import Chunk, Symbol, SymbolChunk
from .template import PlainText, TemplatePart, Variable


@dataclass(frozen=True)
class Unique:
    value: SymbolChunk
    id: int

    def to_template(self) -> TemplatePart:
        return Variable(self.id)

    def is_unique(self) -> Literal[True]:
        return True

    @property
    def size(self) -> int:
        if isinstance(self.value, Symbol):
            return 1
        return len(self.value)


@dataclass(frozen=True)
class Match:
    value: Chunk

    def to_template(self) -> TemplatePart:
        assert not isinstance(self.value, Symbol)
        return PlainText(self.value)

    def is_unique(self) -> Literal[False]:
        return False

    @property
    def size(self) -> int:
        if isinstance(self.value, Symbol):
            return 1
        return len(self.value)


Block = Union[Unique, Match]
