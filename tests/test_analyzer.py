import pytest

from template_analysis import Analyzer, analyze


def test_analyzer_analyze_two_texts() -> None:
    text1 = "A dog is a good pet"
    text2 = "A cat is a good pet"
    result = Analyzer.analyze_two_texts(text1, text2)

    assert result.to_format_string() == "A {} is a good pet"
    assert result.args[0] == ["dog"]
    assert result.args[1] == ["cat"]


def test_analyzer_analyze_1_text() -> None:
    text1 = "A dog is a good pet"
    result = analyze([text1])

    assert result.to_format_string() == "A dog is a good pet"
    assert result.args[0] == []


def test_analyzer_analyze_2_texts() -> None:
    text1 = "A dog is a good pet"
    text2 = "A cat is a good pet"
    result = analyze([text1, text2])

    assert result.to_format_string() == "A {} is a good pet"
    assert result.args[0] == ["dog"]
    assert result.args[1] == ["cat"]


def test_analyzer_analyze_3_texts() -> None:
    text1 = "A dog is a good pet"
    text2 = "A cat is a good pet"
    text3 = "A cat is a pretty pet"
    result = analyze([text1, text2, text3])

    assert result.to_format_string() == "A {} is a {} pet"
    assert result.args[0] == ["dog", "good"]
    assert result.args[1] == ["cat", "good"]
    assert result.args[2] == ["cat", "pretty"]


def test_analyze_more_than_3_texts() -> None:
    with pytest.raises(NotImplementedError):
        analyze(["A", "B", "C", "D"])
