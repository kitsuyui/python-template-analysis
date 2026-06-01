"""Template analysis.

This library does the opposite of template engines.
Template engines take a template and data, and return a formatted string.
This library takes a formatted string and returns a template and data."""

# https://packaging-guide.openastronomy.org/en/latest/advanced/versioning.html
from ._version import __version__
from .analyzer import Analyzer, AnalyzerResult, analyze
from .symbol import Chunks, Symbol, SymbolString, SymbolTable
from .template import PlainText, Template, TemplatePart, Variable

__all__ = [
    "Analyzer",
    "AnalyzerResult",
    "Chunks",
    "PlainText",
    "Symbol",
    "SymbolString",
    "SymbolTable",
    "Template",
    "TemplatePart",
    "Variable",
    "__version__",
    "analyze",
]
