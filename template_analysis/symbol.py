from __future__ import annotations

from dataclasses import dataclass
from typing import Union

Character = str
Chunk = str


@dataclass(frozen=True)
class Symbol:
    value: object

    @classmethod
    def create(cls) -> Symbol:
        return cls(object())


@dataclass
class SymbolTable:
    table: dict[Symbol, Chunk]

    @classmethod
    def create(cls) -> SymbolTable:
        return cls({})

    def add(self, symbol: Symbol, chunk: Chunk) -> None:
        self.table[symbol] = chunk

    def lookup(self, symbol_or_chunk: SymbolChunk) -> Chunk:
        if symbol_or_chunk in self.table:
            assert isinstance(symbol_or_chunk, Symbol)
            return self.table[symbol_or_chunk]
        assert isinstance(symbol_or_chunk, Chunk)
        return symbol_or_chunk


SymbolOrCharacter = Union[Symbol, Character]
SymbolChunk = Union[Symbol, Chunk]
SymbolString = list[SymbolOrCharacter]
SymbolChunks = list[SymbolChunk]


def to_symbol_chunks(
    symbol_string: SymbolString,
) -> SymbolChunks:
    x: SymbolChunks = []
    chunk: str = ""
    for symbol_or_character in symbol_string:
        if isinstance(symbol_or_character, Symbol):
            if chunk:
                x.append(chunk)
                chunk = ""
            x.append(symbol_or_character)
        else:
            chunk += symbol_or_character
    if chunk:
        x.append(chunk)
    return x
