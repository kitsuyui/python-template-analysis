"""Template analysis.

This library does the opposite of template engines.
Template engines take a template and data, and return a formatted string.
This library takes a formatted string and returns a template and data."""

# https://packaging-guide.openastronomy.org/en/latest/advanced/versioning.html
from ._version import __version__
from .analyzer import Analyzer, AnalyzerResult, analyze

__all__ = [
    "Analyzer",
    "AnalyzerResult",
    "__version__",
    "analyze",
]
