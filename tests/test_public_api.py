import template_analysis
from template_analysis import (
    Chunks,
    PlainText,
    Symbol,
    SymbolString,
    SymbolTable,
    Template,
    TemplatePart,
    Variable,
)


def test_analyzer_result_return_types_are_public() -> None:
    expected_exports = {
        "Chunks",
        "PlainText",
        "Symbol",
        "SymbolString",
        "SymbolTable",
        "Template",
        "TemplatePart",
        "Variable",
    }

    assert expected_exports <= set(template_analysis.__all__)


def test_public_return_type_imports_resolve() -> None:
    symbol = Symbol.create()
    symbol_string: SymbolString = [symbol, "x"]
    chunks: Chunks = ["dog"]
    table = SymbolTable.create()
    template = Template([PlainText("A "), Variable(0)])
    template_part: TemplatePart = PlainText("part")

    assert symbol_string == [symbol, "x"]
    assert chunks == ["dog"]
    assert table.lookup("cat") == "cat"
    assert template.to_format_string() == "A {0}"
    assert template_part.to_format_string() == "part"
