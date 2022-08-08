from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Union

from .symbol import Chunk, Symbol, SymbolString, SymbolTable


@dataclass(frozen=True)
class Variable:
    id: int

    def to_format_string(self) -> str:
        return "{}"

    def is_variable(self) -> Literal[True]:
        return True

    def is_plain_text(self) -> Literal[False]:
        return False


@dataclass(frozen=True)
class PlainText:
    value: str

    def to_format_string(self) -> str:
        return self.value

    def is_variable(self) -> Literal[False]:
        return False

    def is_plain_text(self) -> Literal[True]:
        return True


TemplatePart = Union[PlainText, Variable]


@dataclass(frozen=True)
class Template:
    parts: list[TemplatePart]

    def to_format_string(self) -> str:
        return "".join(part.to_format_string() for part in self.parts)

    def remap_to_symbols(
        self, args: list[list[Chunk]]
    ) -> tuple[SymbolString, list[SymbolTable]]:
        seq: SymbolString = []
        tables: list[SymbolTable] = [
            SymbolTable.create() for _ in enumerate(args)
        ]
        args = [arg[:] for arg in args]
        for part in self.parts:
            if part.is_variable():
                symbol = Symbol.create()
                for table, arg in zip(tables, args):
                    table.add(symbol, arg[0])
                    arg.pop(0)
                seq.append(symbol)
            elif part.is_plain_text():
                assert isinstance(part, PlainText)
                for char in part.value:
                    seq.append(char)
        return seq, tables
