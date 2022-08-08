from template_analysis.symbol import Symbol, SymbolTable, to_symbol_chunks


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
    table.add(symbol1, "a")

    assert table.lookup(symbol1) == "a"
    assert table.lookup("b") == "b"
