import pytest

from template_analysis.symbol import (
    Symbol,
    SymbolTable,
    SymbolTemplate,
    to_symbol_chunks,
)


def test_to_symbol_chunks() -> None:
    symbol1 = Symbol.create()
    symbol2 = Symbol.create()

    assert to_symbol_chunks(["a", "b", "c"]) == ["abc"]
    assert to_symbol_chunks(["a", "b", symbol1]) == [
        "ab",
        symbol1,
    ]

    assert to_symbol_chunks(["a", "b", symbol1, "c", "d"]) == [
        "ab",
        symbol1,
        "cd",
    ]

    assert to_symbol_chunks([symbol1, "a", "b", symbol2, "c", "d"]) == [
        symbol1,
        "ab",
        symbol2,
        "cd",
    ]


def test_symbol_table() -> None:
    table = SymbolTable.create()
    symbol1 = Symbol.create()
    table = table.add(symbol1, "a")

    assert table.lookup(symbol1) == "a"
    assert table.lookup("b") == "b"


def test_symbol_table_lookup_missing_symbol() -> None:
    table = SymbolTable.create()
    unknown = Symbol.create()
    with pytest.raises(KeyError, match=r"Symbol not found in table"):
        table.lookup(unknown)


def test_symbol_table_combined_normalizes_chains() -> None:
    # table_a: s1 -> "value"
    table_a = SymbolTable.create()
    s1 = Symbol.create()
    table_a = table_a.add(s1, "value")

    # table_b: s2 -> s1 (chain s2 -> s1 -> "value")
    table_b = SymbolTable.create()
    s2 = Symbol.create()
    table_b = table_b.add(s2, s1)

    combined = table_a.combined(table_b)
    assert combined.lookup(s1) == "value"
    assert combined.lookup(s2) == "value"
    # The combined table must store the resolved chunk directly (depth 1).
    assert combined.table[s2] == "value"


def test_symbol_table_lookup_composite_symbol_string() -> None:
    table = SymbolTable.create()
    s1 = Symbol.create()
    s2 = Symbol.create()
    table = table.add(s1, "left")
    table = table.add(s2, [s1, "-", "right"])

    assert table.lookup(s2) == "left-right"


def test_symbol_template() -> None:
    template = SymbolTemplate([], SymbolTable.create())
    assert template.resolve() == []
    assert template.args() == []

    template = SymbolTemplate(["a", "b", "c"], SymbolTable.create())
    assert template.resolve() == [
        "a",
        "b",
        "c",
    ]
    assert template.args() == []

    table = SymbolTable.create()
    symbol1 = Symbol.create()
    table = table.add(symbol1, "x")
    template = SymbolTemplate(["a", "b", symbol1, "c", "d"], table)
    assert template.resolve() == ["a", "b", "x", "c", "d"]
    assert template.args() == ["x"]
