from __future__ import annotations

from dataclasses import dataclass

Character = str
Chunk = str


@dataclass(frozen=True)
class Symbol:
    """A symbol in a template."""

    value: object

    @classmethod
    def create(cls) -> Symbol:
        return cls(object())


@dataclass
class SymbolTable:
    """A table of symbols."""

    table: dict[Symbol, SymbolChunk]

    @classmethod
    def create(cls) -> SymbolTable:
        return cls({})

    def add(self, symbol: Symbol, chunk: SymbolChunk) -> None:
        self.table[symbol] = chunk

    def _resolve_symbol(self, symbol: Symbol) -> SymbolChunk:
        resolved = self.table.get(symbol)
        if resolved is None:
            raise KeyError(
                f"Symbol not found in table"
                f" (table size: {len(self.table)})",
            )
        return resolved

    def lookup(self, symbol_or_chunk: SymbolChunk) -> Chunk:
        while isinstance(symbol_or_chunk, Symbol):
            symbol_or_chunk = self._resolve_symbol(symbol_or_chunk)
        if not isinstance(symbol_or_chunk, Chunk):
            raise RuntimeError(
                f"Internal invariant violated: expected Chunk after symbol "
                f"resolution but got {type(symbol_or_chunk).__name__!r}. "
                "This indicates an unresolvable symbol or a cycle.",
            )
        return symbol_or_chunk

    def combined(self, other: SymbolTable) -> SymbolTable:
        merged: dict[Symbol, SymbolChunk] = {**self.table, **other.table}
        merged_table = SymbolTable(merged)
        # Flatten symbol chains to depth 1 so lookup() stays O(1) per call.
        return SymbolTable(
            {s: merged_table.lookup(s) for s in merged},
        )


SymbolOrCharacter = Symbol | Character
SymbolChunk = Symbol | Chunk
Chunks = list[Chunk]
SymbolString = list[SymbolOrCharacter]
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
