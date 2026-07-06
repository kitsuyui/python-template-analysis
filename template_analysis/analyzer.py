from __future__ import annotations

import difflib
import unicodedata
from collections.abc import Iterator
from dataclasses import dataclass

from .symbol import (
    Chunks,
    Symbol,
    SymbolChunk,
    SymbolChunks,
    SymbolString,
    SymbolTable,
    SymbolTemplate,
    to_symbol_chunks,
)
from .template import Template


def chunk_to_symbol_string(chunk: SymbolChunk) -> SymbolString:
    if isinstance(chunk, Symbol):
        return [chunk]
    return list(chunk)


@dataclass(frozen=True, eq=False)
class AnalyzerResult:
    """Result of analyzing a list of texts for a common template pattern.

    Attributes:
        text: Symbolic string representing the generalized template structure.
        tables: One symbol table per analyzed text, mapping symbols to their
            concrete values in that text.

    Example:
        >>> result = analyze(["Hello Alice", "Hello Bob"])
        >>> result.to_format_string()
        'Hello {0}'
        >>> result.args[0]
        ['Alice']
        >>> result.args[1]
        ['Bob']

    """

    text: SymbolString
    tables: list[SymbolTable]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AnalyzerResult):
            return NotImplemented
        return (
            self.to_format_string() == other.to_format_string()
            and self.args == other.args
        )

    def __hash__(self) -> int:
        return hash(
            (self.to_format_string(), tuple(tuple(a) for a in self.args)),
        )

    @property
    def template(self) -> Template:
        return Template.from_symbol_template(
            SymbolTemplate(self.text[:], SymbolTable.create()),
        )

    @property
    def args(self) -> list[Chunks]:
        return [
            SymbolTemplate(self.text[:], table).args() for table in self.tables
        ]

    def to_format_string(self) -> str:
        return self.template.to_format_string()

    @classmethod
    def _from_text(cls, text: str) -> AnalyzerResult:
        return AnalyzerResult(
            text=list(unicodedata.normalize("NFC", text)),
            tables=[SymbolTable.create()],
        )


@dataclass
class Analyzer:
    """Stateful parser that identifies common patterns across texts.

    This is the internal implementation class. Use the module-level
    ``analyze`` function or ``Analyzer.analyze`` classmethod for the
    public API.
    """

    text: SymbolString
    pos: int
    parsed: SymbolChunks
    table: SymbolTable

    @classmethod
    def create(cls, text: str | SymbolString) -> Analyzer:
        return cls(
            list(text),
            pos=0,
            parsed=[],
            table=SymbolTable.create(),
        )

    def _proceed(self, size: int) -> None:
        self.pos += size

    @property
    def parsed_text(self) -> SymbolString:
        return [
            symbol_or_character
            for chunk in self.parsed
            for symbol_or_character in chunk_to_symbol_string(chunk)
        ]

    def __read_n_tokens(self, size: int) -> Iterator[SymbolChunk]:
        start = self.pos
        stop = self.pos + size
        token: SymbolString = self.text[start:stop]
        for s in to_symbol_chunks(token):
            if isinstance(s, Symbol):
                self._proceed(1)
            else:
                self._proceed(len(s))
            yield s

    def _append_match(self, size: int) -> None:
        for s in self.__read_n_tokens(size):
            self.parsed.append(s)

    def _append_unique(self, size: int, symbol: Symbol) -> None:
        for s in self.__read_n_tokens(size):
            self.parsed.append(symbol)
            self.table.add(symbol, s)

    def _append_unique_or_empty(self, size: int, symbol: Symbol) -> None:
        if size == 0:
            self.parsed.append(symbol)
            self.table.add(symbol, "")
            return
        self._append_unique(size, symbol)

    def _advance(
        self,
        pos: int,
        size: int,
        symbol: Symbol,
        force_unique: bool = False,
    ) -> None:
        unmatch_length = pos - self.pos
        if force_unique or unmatch_length > 0:
            self._append_unique_or_empty(unmatch_length, symbol)
        self._append_match(size)

    @classmethod
    def _analyze_two_symbol_strings(
        cls, seq1: SymbolString, seq2: SymbolString,
    ) -> tuple[Analyzer, Analyzer]:
        matcher = difflib.SequenceMatcher(None, seq1, seq2, autojunk=False)
        blocks = matcher.get_matching_blocks()
        # SequenceMatcher guarantees a sentinel (len(seq1), len(seq2), 0) that
        # drives tail content through advance() to complete both analyzers.
        sentinel = blocks[-1] if blocks else None
        if sentinel is None or (sentinel.a, sentinel.b, sentinel.size) != (
            len(seq1),
            len(seq2),
            0,
        ):
            msg = (
                "get_matching_blocks() must end with the sentinel "
                "(len(seq1), len(seq2), 0); tail content would be dropped "
                "without it."
            )
            raise RuntimeError(msg)
        analyzer_a = cls.create(seq1)
        analyzer_b = cls.create(seq2)

        for block in blocks:
            symbol = Symbol.create()
            unmatch_a = block.a - analyzer_a.pos
            unmatch_b = block.b - analyzer_b.pos
            force_unique = unmatch_a > 0 or unmatch_b > 0
            analyzer_a._advance(
                block.a,
                block.size,
                symbol,
                force_unique,
            )
            analyzer_b._advance(
                block.b,
                block.size,
                symbol,
                force_unique,
            )

        return analyzer_a, analyzer_b

    @classmethod
    def analyze(
        cls,
        texts: list[str],
        max_texts: int | None = None,
    ) -> AnalyzerResult:
        """Analyze a list of texts and extract a common template.

        Args:
            texts: Non-empty list of strings to analyze.
            max_texts: Optional upper bound on the number of texts to analyze.

        Returns:
            An AnalyzerResult containing the extracted template and per-text
            argument lists.

        Raises:
            ValueError: If texts is empty or exceeds max_texts.

        """
        return cls._analyze_texts(texts, max_texts=max_texts)

    @classmethod
    def _analyze_two_result(
        cls, result1: AnalyzerResult, result2: AnalyzerResult,
    ) -> AnalyzerResult:
        analyzer_a, analyzer_b = cls._analyze_two_symbol_strings(
            result1.text, result2.text,
        )
        if analyzer_a.parsed_text != analyzer_b.parsed_text:
            raise RuntimeError(
                "Internal invariant violated: both analyzers must produce "
                "the same parsed_text. This indicates a bug in the analysis "
                f"algorithm. Got: {analyzer_a.parsed_text!r} vs "
                f"{analyzer_b.parsed_text!r}",
            )
        return AnalyzerResult(
            analyzer_a.parsed_text,
            [
                *[
                    analyzer_a.table.combined(table)
                    for table in result1.tables
                ],
                *[
                    analyzer_b.table.combined(table)
                    for table in result2.tables
                ],
            ],
        )

    @staticmethod
    def _assert_max_texts(n: int, max_texts: int | None) -> None:
        if max_texts is not None and n > max_texts:
            raise ValueError(
                f"Too many texts: got {n}, max_texts={max_texts}. "
                "analyze_texts holds O(N) SymbolTable entries in memory.",
            )

    @classmethod
    def _analyze_texts(
        cls,
        texts: list[str],
        max_texts: int | None = None,
    ) -> AnalyzerResult:
        texts = texts[:]

        if not texts:
            raise ValueError("texts are empty.")

        cls._assert_max_texts(len(texts), max_texts)

        text = texts.pop(0)
        acc = AnalyzerResult._from_text(text)
        while texts:
            text = texts.pop(0)
            curr = AnalyzerResult._from_text(text)
            acc = cls._analyze_two_result(acc, curr)

        return acc


analyze = Analyzer.analyze
