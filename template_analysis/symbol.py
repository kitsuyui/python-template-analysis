from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType

Character = str
Chunk = str


@dataclass(frozen=True)
class Symbol:
    """A symbol in a template."""

    value: object = field(repr=False)

    @classmethod
    def create(cls) -> Symbol:
        return cls(object())

    def __repr__(self) -> str:
        return "Symbol()"


@dataclass
class SymbolTable:
    """A table of symbols."""

    table: Mapping[Symbol, SymbolValue]

    @classmethod
    def create(cls) -> SymbolTable:
        empty: dict[Symbol, SymbolValue] = {}
        return cls(MappingProxyType(empty))

    def add(self, symbol: Symbol, chunk: SymbolValue) -> SymbolTable:
        new: dict[Symbol, SymbolValue] = {**self.table, symbol: chunk}
        return SymbolTable(MappingProxyType(new))

    def _resolve_symbol(self, symbol: Symbol) -> SymbolValue:
        resolved = self.table.get(symbol)
        if resolved is None:
            raise KeyError(
                f"Symbol not found in table"
                f" (table size: {len(self.table)})",
            )
        return resolved

    def lookup(self, symbol_or_chunk: SymbolChunk) -> Chunk:
        resolved = self._resolve_value(symbol_or_chunk)
        if not isinstance(resolved, Chunk):
            raise RuntimeError(
                f"Internal invariant violated: expected Chunk after symbol "
                f"resolution but got {type(resolved).__name__!r}. "
                "This indicates an unresolvable symbol or a cycle.",
            )
        return resolved

    def _resolve_value(self, value: SymbolValue) -> Chunk:
        while isinstance(value, Symbol):
            value = self._resolve_symbol(value)
        if isinstance(value, list):
            return "".join(self._resolve_value(chunk) for chunk in value)
        return value

    def combined(self, other: SymbolTable) -> SymbolTable:
        merged: dict[Symbol, SymbolValue] = {**self.table, **other.table}
        merged_table = SymbolTable(MappingProxyType(merged))
        # Flatten symbol chains to depth 1 so lookup() stays O(1) per call.
        return SymbolTable(
            MappingProxyType({s: merged_table.lookup(s) for s in merged}),
        )


SymbolOrCharacter = Symbol | Character
SymbolChunk = Symbol | Chunk
Chunks = list[Chunk]
SymbolString = list[SymbolOrCharacter]
SymbolValue = SymbolChunk | SymbolString
SymbolChunks = list[SymbolChunk]


def append_chunk(symbol_chunks: SymbolChunks, chunk: Chunk) -> Chunk:
    if chunk:
        symbol_chunks.append(chunk)
    return ""


def to_symbol_chunks(
    symbol_string: SymbolString,
) -> SymbolChunks:
    symbol_chunks: SymbolChunks = []
    chunk: str = ""
    for symbol_or_character in symbol_string:
        if isinstance(symbol_or_character, Symbol):
            chunk = append_chunk(symbol_chunks, chunk)
            symbol_chunks.append(symbol_or_character)
            continue
        chunk += symbol_or_character
    append_chunk(symbol_chunks, chunk)
    return symbol_chunks


@dataclass(frozen=True)
class SymbolTemplate:
    text: SymbolChunks
    table: SymbolTable

    def resolve(self) -> Chunks:
        return [self.table.lookup(chunk) for chunk in self.text]

    def args(self) -> list[Chunk]:
        return [
            self.table.lookup(chunk)
            for chunk in self.text
            if isinstance(chunk, Symbol)
        ]
