import pytest

from template_analysis import analyze


def test_analyzer_analyze_0_text() -> None:
    with pytest.raises(ValueError) as e:
        analyze([])

    assert str(e.value) == "texts are empty."


def test_analyzer_analyze_1_text() -> None:
    text1 = "A dog is a good pet"
    result = analyze([text1])

    assert result.to_format_string() == "A dog is a good pet"
    assert result.args[0] == []


def test_analyzer_analyze_2_texts() -> None:
    text1 = "A dog is a good pet"
    text2 = "A cat is a good pet"
    result = analyze([text1, text2])

    assert result.to_format_string() == "A {0} is a good pet"
    assert result.args[0] == ["dog"]
    assert result.args[1] == ["cat"]


def test_analyzer_analyze_2_texts_with_empty_variable() -> None:
    result = analyze(["axb", "ab"])

    assert result.to_format_string() == "a{0}b"
    assert result.args[0] == ["x"]
    assert result.args[1] == [""]


def test_analyzer_analyze_2_texts_with_empty_variable_first() -> None:
    result = analyze(["ab", "axb"])

    assert result.to_format_string() == "a{0}b"
    assert result.args[0] == [""]
    assert result.args[1] == ["x"]


def test_analyzer_analyze_3_texts() -> None:
    text1 = "A dog is a good pet"
    text2 = "A cat is a good pet"
    text3 = "A cat is a pretty pet"
    result = analyze([text1, text2, text3])

    assert result.to_format_string() == "A {0} is a {1} pet"
    assert result.args[0] == ["dog", "good"]
    assert result.args[1] == ["cat", "good"]
    assert result.args[2] == ["cat", "pretty"]


def test_analyzer_analyze_4_texts() -> None:
    text1 = "A dog is a good pet"
    text2 = "A cat is a good pet"
    text3 = "A cat is a pretty pet"
    text4 = "A bird is a great pet"
    result = analyze([text1, text2, text3, text4])

    assert result.to_format_string() == "A {0} is a {1} pet"
    assert result.args[0] == ["dog", "good"]
    assert result.args[1] == ["cat", "good"]
    assert result.args[2] == ["cat", "pretty"]
    assert result.args[3] == ["bird", "great"]


def test_analyzer_result_equality_across_calls() -> None:
    texts = ["A dog is a good pet", "A cat is a good pet"]
    r1 = analyze(texts)
    r2 = analyze(texts)
    assert r1 == r2
    assert hash(r1) == hash(r2)


def test_analyzer_result_inequality_different_inputs() -> None:
    r1 = analyze(["A dog is a good pet", "A cat is a good pet"])
    r2 = analyze(["A dog is a good pet", "A fish is a good pet"])
    assert r1 != r2


def test_analyzer_analyze_long_texts_autojunk_disabled() -> None:
    # Texts over 200 chars with high-frequency chars (space ~50%) triggered
    # SequenceMatcher autojunk, causing the shared prefix to be excluded from
    # matching and incorrectly detected as a variable. autojunk=False prevents this.
    prefix = "a " * 95  # 190 chars; 'a' and ' ' each appear ~50% — autojunk candidates
    text1 = prefix + "dog"
    text2 = prefix + "cat"
    result = analyze([text1, text2])

    assert result.to_format_string() == prefix + "{0}"
    assert result.args[0] == ["dog"]
    assert result.args[1] == ["cat"]
