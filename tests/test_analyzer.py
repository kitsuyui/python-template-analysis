import pytest

from template_analysis import Analyzer, analyze


def test_analyzer_analyze_two_strings() -> None:
    string1 = "A dog is a good pet"
    string2 = "A cat is a good pet"
    result = Analyzer.analyze_two_strings(string1, string2)

    assert result.to_format_string() == "A {} is a good pet"
    assert result.args[0] == ["dog"]
    assert result.args[1] == ["cat"]


def test_analyzer_analyze_1_string() -> None:
    string1 = "A dog is a good pet"
    result = analyze([string1])

    assert result.to_format_string() == "A dog is a good pet"
    assert result.args[0] == []


def test_analyzer_analyze_2_strings() -> None:
    string1 = "A dog is a good pet"
    string2 = "A cat is a good pet"
    result = analyze([string1, string2])

    assert result.to_format_string() == "A {} is a good pet"
    assert result.args[0] == ["dog"]
    assert result.args[1] == ["cat"]


def test_analyzer_analyze_3_strings() -> None:
    string1 = "A dog is a good pet"
    string2 = "A cat is a good pet"
    string3 = "A cat is a pretty pet"
    result = analyze([string1, string2, string3])

    assert result.to_format_string() == "A {} is a {} pet"
    assert result.args[0] == ["dog", "good"]
    assert result.args[1] == ["cat", "good"]
    assert result.args[2] == ["cat", "pretty"]


def test_analyze_more_than_3_strings() -> None:
    with pytest.raises(NotImplementedError):
        analyze(["A", "B", "C", "D"])
