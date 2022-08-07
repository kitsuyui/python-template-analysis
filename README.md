# template-analysis

This repo provides template analysis tool.

1. Untemplate
2. Template deriving (by content and parameter)
3. Template deriving (by same parts of contents)
4. Automated scraping (1 + 2 or 3)

## Concept images

![1-templating](https://user-images.githubusercontent.com/2596972/73120667-7bafbf80-3fb4-11ea-823f-263c0010e0e9.png)
![2-untemplating](https://user-images.githubusercontent.com/2596972/73120668-7bafbf80-3fb4-11ea-9426-5471fcf2e601.png)
![3-template-deriving](https://user-images.githubusercontent.com/2596972/73120669-7bafbf80-3fb4-11ea-8236-1ab68f75ce60.png)
![4-template-deriving-2](https://user-images.githubusercontent.com/2596972/73120670-7c485600-3fb4-11ea-9eba-01aaafd08e4e.png)
![4-automated-scraping](https://user-images.githubusercontent.com/2596972/73120671-7c485600-3fb4-11ea-8ed6-56b93ee99b3a.png)

## Usage

```python
>>> from template_analysis import Analyzer
>>> string1 = 'A dog is a good pet'
>>> string2 = 'A cat is a good pet'
>>> result = Analyzer.analyze([string1, string2])
>>> result.to_format_string()
'A {} is a good pet'
>>> result.args[0]
['dog']
>>> result.args[1]
['cat']
```

## Development plan

Phase 1: Develop all of the features with Python for proof of concept.
Phase 2: Rewrite with performance focused language (based on the result of phase 1).

## License

The 3-Clause BSD License. See also LICENSE file.
