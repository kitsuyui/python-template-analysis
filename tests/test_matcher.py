from template_analysis.matcher import Match, Unique
from template_analysis.template import PlainText, Variable


def test_unique() -> None:
    unique = Unique("dog", 0)
    assert unique.to_template() == Variable(0)
    assert unique.is_unique() is True
    assert unique.to_string() == "dog"


def test_match() -> None:
    match = Match("dog")
    assert match.to_template() == PlainText("dog")
    assert match.is_unique() is False
    assert match.to_string() == "dog"
