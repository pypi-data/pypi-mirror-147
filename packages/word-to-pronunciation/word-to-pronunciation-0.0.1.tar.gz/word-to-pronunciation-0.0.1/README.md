# word-to-pronunciation

[![PyPI](https://img.shields.io/pypi/v/word-to-pronunciation.svg)](https://pypi.python.org/pypi/word-to-pronunciation)
[![PyPI](https://img.shields.io/pypi/pyversions/word-to-pronunciation.svg)](https://pypi.python.org/pypi/word-to-pronunciation)
[![MIT](https://img.shields.io/github/license/stefantaubert/sentence2pronunciation.svg)](LICENSE)

Python library to help with looking up words that contain punctuation and hyphens.

## Installation

```sh
pip install word-to-pronunciation
```

## Usage

```python
>>> from collections import OrderedDict
>>> from pronunciation_dictionary import Pronunciations, Word
>>> from word_to_pronunciation import Options, get_cached_lookup, get_pronunciations_from_word

>>> def lookup(word: Word) -> Pronunciations:
...   print(f"Trying to lookup: '{word}' ...")
...   if word == "test":
...     result = OrderedDict((
...       (("T", "E0", "S", "T"), 0.7),
...       (("T", "E1", "S", "T"), 0.3),
...     ))
...     print("Found pronunciations!")
...     return result
...   print("Found no pronunciations!")
...   return OrderedDict()

>>> options = Options(
...   trim_symbols="\".",
...   split_on_hyphen=True,
...   try_without_trimming=True,
...   try_without_splitting=True,
...   default_weight=1.0
... )

>>> cache = {}
>>> lookup_method = get_cached_lookup(lookup, cache)

>>> word = "\"test-test\"."
>>> result = get_pronunciations_from_word(word, lookup_method, options)
Trying to lookup: '"test-test".' ...
Found no pronunciations!
Trying to lookup: 'test-test' ...
Found no pronunciations!
Trying to lookup: 'test' ...
Found pronunciations!

>>> for pronunciation, weight in result.items():
...   print(f"{word} => /{'|'.join(pronunciation)}/ {weight}")
"test-test". => /"|T|E0|S|T|-|T|E0|S|T|"|./ 0.48999999999999994
"test-test". => /"|T|E0|S|T|-|T|E1|S|T|"|./ 0.21
"test-test". => /"|T|E1|S|T|-|T|E0|S|T|"|./ 0.21
"test-test". => /"|T|E1|S|T|-|T|E1|S|T|"|./ 0.09

>>> print(cache)
{'"test-test".': OrderedDict(), 'test-test': OrderedDict(), 'test': OrderedDict([(('T', 'E0', 'S', 'T'), 0.7), (('T', 'E1', 'S', 'T'), 0.3)])}
```
