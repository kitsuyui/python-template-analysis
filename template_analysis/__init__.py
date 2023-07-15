"""Template analysis.

This library does the opposite of template engines.
Template engines take a template and data, and return a formatted string.
This library takes a formatted string and returns a template and data."""
from .analyzer import Analyzer, AnalyzerResult, analyze  # noqa: F401
