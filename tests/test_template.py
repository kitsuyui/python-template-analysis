from template_analysis.template import PlainText, Template, Variable


def test_variable_to_format_string() -> None:
    variable = Variable(0)
    assert variable.to_format_string() == "{0}"


def test_variable_to_format_string_id_reflected() -> None:
    assert Variable(1).to_format_string() == "{1}"
    assert Variable(2).to_format_string() == "{2}"


def test_plain_text_to_format_string() -> None:
    text = PlainText("dog")
    assert text.to_format_string() == "dog"


def test_plain_text_to_format_string_escapes_literal_braces() -> None:
    text = PlainText("{name} -> {value}")
    assert text.to_format_string() == "{{name}} -> {{value}}"


def test_template_to_format_string() -> None:
    template = Template([PlainText("cogito "), Variable(0), PlainText(" sum")])
    assert template.to_format_string() == "cogito {0} sum"


def test_template_to_format_string_preserves_literal_braces() -> None:
    template = Template(
        [
            PlainText("{name} is a "),
            Variable(0),
            PlainText(" in {group}"),
        ],
    )

    format_string = template.to_format_string()

    assert format_string.startswith("{{name}} is a ")
    assert format_string.endswith(" in {{group}}")
    assert format_string.format("dog") == "{name} is a dog in {group}"
