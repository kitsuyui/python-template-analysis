from __future__ import annotations

import difflib
from dataclasses import dataclass
from typing import Literal, Union

from .matcher import Block, Match, Unique
from .symbol import (
    Chunk,
    Symbol,
    SymbolChunk,
    SymbolString,
    SymbolTable,
    to_symbol_chunks,
)
from .template import PlainText, Template


@dataclass(frozen=True)
class AnalyzerResult:
    template: Template
    args: list[list[str]]

    def to_format_string(self) -> str:
        return self.template.to_format_string()

    def conv(self) -> tuple[SymbolString, list[SymbolTable]]:
        return self.template.remap_to_symbols(self.args)

    @classmethod
    def from_text(cls, text: str) -> AnalyzerResult:
        return AnalyzerResult(
            template=Template([PlainText(text)]),
            args=[[]],
        )

    @classmethod
    def from_template(
        cls, template: Template, args: list[list[str]]
    ) -> AnalyzerResult:
        return AnalyzerResult(template, args)


@dataclass
class Analyzer:
    text: SymbolString
    pos: int
    count_unique: int
    blocks: list[Block]

    @classmethod
    def create(cls, text: Union[str, SymbolString]) -> Analyzer:
        return cls(list(text), pos=0, count_unique=0, blocks=[])

    def proceed(self, size: int) -> None:
        self.pos += size

    def append_match(self, text: Chunk) -> None:
        match = Match(text)
        self.blocks.append(match)
        self.proceed(match.size)

    def append_unique(self, text: SymbolChunk) -> None:
        unique = Unique(text, self.count_unique)
        self.blocks.append(unique)
        self.count_unique += 1
        self.proceed(unique.size)

    def append(self, type: Literal["match", "unique"], size: int) -> None:
        if size == 0:
            return

        start = self.pos
        stop = self.pos + size
        token: SymbolString = self.text[start:stop]

        if type == "match":
            for s in to_symbol_chunks(token):
                assert not isinstance(s, Symbol)
                self.append_match(s)
        elif type == "unique":
            for s in to_symbol_chunks(token):
                self.append_unique(s)

    def to_template(self) -> Template:
        return Template([block.to_template() for block in self.blocks])

    def to_args(self) -> list[Chunk]:
        return [str(chunk) for chunk in self.to_uniques()]

    def to_uniques(self) -> list[SymbolChunk]:
        return [block.value for block in self.blocks if block.is_unique()]

    def to_args_lookup_by_symbol_table(
        self, table: SymbolTable
    ) -> list[Chunk]:
        return [table.lookup(arg) for arg in self.to_uniques()]

    def advance(self, pos: int, size: int) -> None:
        while (unmatch_length := pos - self.pos) > 0:
            self.append("unique", unmatch_length)
        self.append("match", size)

    @classmethod
    def analyze_two_symbol_strings(
        cls, seq1: SymbolString, seq2: SymbolString
    ) -> tuple[Analyzer, Analyzer]:
        matcher = difflib.SequenceMatcher(None, seq1, seq2)
        blocks = matcher.get_matching_blocks()
        analyzer_a = cls.create(seq1)
        analyzer_b = cls.create(seq2)

        for block in blocks:
            analyzer_a.advance(block.a, block.size)
            analyzer_b.advance(block.b, block.size)

        template_a = analyzer_a.to_template()
        template_b = analyzer_b.to_template()
        assert template_a == template_b, (
            "Guessed templates are mismatch: " f"{template_a} != {template_b}"
        )

        return analyzer_a, analyzer_b

    @classmethod
    def analyze(cls, texts: list[str]) -> AnalyzerResult:
        if len(texts) == 1:
            return AnalyzerResult.from_text(texts[0])
        elif len(texts) == 2:
            return cls.analyze_two_texts(texts[0], texts[1])
        elif len(texts) == 3:
            return cls.analyze_three_texts(texts[0], texts[1], texts[2])

        raise NotImplementedError(
            "Analyze more than three strings are not implemented yet."
        )

    @classmethod
    def analyze_two_texts(cls, text1: str, text2: str) -> AnalyzerResult:
        analyzer_a, analyzer_b = cls.analyze_two_symbol_strings(
            list(text1), list(text2)
        )
        template_a = analyzer_a.to_template()
        vars_a = analyzer_a.to_args()[:]
        vars_b = analyzer_b.to_args()[:]
        return AnalyzerResult.from_template(template_a, [vars_a, vars_b])

    @classmethod
    def analyze_two_result(
        cls, result1: AnalyzerResult, result2: AnalyzerResult
    ) -> AnalyzerResult:
        seq1, tables1 = result1.conv()
        seq2, tables2 = result2.conv()
        analyzer_a, analyzer_b = cls.analyze_two_symbol_strings(seq1, seq2)
        template_a = analyzer_a.to_template()
        args1 = [
            analyzer_a.to_args_lookup_by_symbol_table(table)
            for table in tables1
        ]
        args2 = [
            analyzer_b.to_args_lookup_by_symbol_table(table)
            for table in tables2
        ]
        return AnalyzerResult.from_template(template_a, [*args1, *args2])

    @classmethod
    def analyze_three_texts(
        cls, text1: str, text2: str, text3: str
    ) -> AnalyzerResult:
        result_1_and_2 = cls.analyze_two_texts(text1, text2)
        result_2_and_3 = cls.analyze_two_texts(text2, text3)
        result_3_and_1 = cls.analyze_two_texts(text3, text1)
        r1 = cls.analyze_two_result(result_1_and_2, result_2_and_3)
        r2 = cls.analyze_two_result(result_2_and_3, result_3_and_1)
        rx = cls.analyze_two_result(r1, r2)
        assert rx.args[1] == rx.args[2]
        return AnalyzerResult.from_template(
            rx.template,
            [
                rx.args[0],
                rx.args[1],
                rx.args[3],
            ],
        )


analyze = Analyzer.analyze
