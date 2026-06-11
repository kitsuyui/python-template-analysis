# template-analysis

[![Python](https://img.shields.io/pypi/pyversions/template-analysis.svg)](https://badge.fury.io/py/template-analysis)
[![PyPI version](https://img.shields.io/pypi/v/template-analysis.svg)](https://pypi.python.org/pypi/template-analysis/)
![Coverage](https://raw.githubusercontent.com/kitsuyui/octocov-central/main/badges/kitsuyui/python-template-analysis/coverage.svg)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

Generate template and extract variables from texts.
In other words, template-analysis makes reverse template (untemplate).

## Usage

Currently, this supports analyzing one or more texts.

```python
from template_analysis import analyze
result = analyze([
    "A dog is a good pet",
    "A cat is a good pet",
    "A cat is a pretty pet",
    "A bird is a great pet",
])
result.to_format_string()  # => "A {0} is a {1} pet"
result.args[0]  # => ["dog", "good"]
result.args[1]  # => ["cat", "good"]
result.args[2]  # => ["cat", "pretty"]
result.args[3]  # => ["bird", "great"]
```

## Concepts / Future plans

### Development plans

- [x] 1. Untemplate two texts.
- [x] 2. Untemplate multiple / complex texts.
- [ ] 3. Untemplate nested / tree-structured texts.
- [ ] 4. Support several features for scraping.
- [ ] 5. Implement a more efficient algorithm.

### Image boards

![1-templating](https://user-images.githubusercontent.com/2596972/73120667-7bafbf80-3fb4-11ea-823f-263c0010e0e9.png)
![2-untemplating](https://user-images.githubusercontent.com/2596972/73120668-7bafbf80-3fb4-11ea-9426-5471fcf2e601.png)
![3-template-deriving](https://user-images.githubusercontent.com/2596972/73120669-7bafbf80-3fb4-11ea-8236-1ab68f75ce60.png)
![4-template-deriving-2](https://user-images.githubusercontent.com/2596972/73120670-7c485600-3fb4-11ea-9eba-01aaafd08e4e.png)
![4-automated-scraping](https://user-images.githubusercontent.com/2596972/73120671-7c485600-3fb4-11ea-8ed6-56b93ee99b3a.png)

## Development

This repository uses [lefthook](https://lefthook.dev/) to run the same checks as CI
locally, so problems surface before they reach CI.

```sh
# Install dependencies
uv sync

# Install the Git hooks (once; requires lefthook on your PATH)
lefthook install
```

Once installed, the hooks run automatically:

- **pre-commit**: `uv run poe check`
- **pre-push**: `uv run poe check` and `uv run poe test`

You can also run the checks manually:

```sh
uv run poe check
uv run poe test
```

CI still runs the full matrix (see `.github/workflows/`); the hooks only bring that
feedback earlier on your machine.

## Release notes

See [CHANGELOG.md](CHANGELOG.md) for release history and upgrade notes.

## License

The 3-Clause BSD License. See also LICENSE file.
