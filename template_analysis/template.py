from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from .symbol import Symbol, SymbolTemplate


@dataclass(frozen=True)
class Variable:
    """A extracted variable in a template."""

    id: int

    def to_format_string(self) -> str:
        return "{}"


@dataclass(frozen=True)
class PlainText:
    """A plain text chunk in a template."""

    value: str

    def to_format_string(self) -> str:
        return self.value


# A part of a template is either a plain text chunk or a variable.
TemplatePart = Union[PlainText, Variable]


@dataclass(frozen=True)
class Template:
    """A template extracted from a formatted string.

    A template is a list of parts,
    where each part is either a plain text chunk or a variable.
    """

    parts: list[TemplatePart]

    @classmethod
    def from_symbol_template(cls, st: SymbolTemplate) -> Template:
        parts: list[TemplatePart] = []
        variables = 0
        for chunk in st.text:
            if isinstance(chunk, Symbol):
                parts.append(Variable(variables))
                variables += 1
            else:
                parts.append(PlainText(chunk))
        return cls(parts)

    def to_format_string(self) -> str:
        return "".join(part.to_format_string() for part in self.parts)
