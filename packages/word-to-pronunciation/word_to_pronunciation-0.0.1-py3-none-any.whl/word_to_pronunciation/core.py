from collections import OrderedDict
from dataclasses import dataclass
from typing import Generator, List, Optional, Tuple

from pronunciation_dictionary import Pronunciation, Pronunciations, Weight, Word

from word_to_pronunciation.types import LookupMethod
from word_to_pronunciation.utils import separate_symbols, symbols_join

HYPHEN = "-"


@dataclass()
class Options():
  trim_symbols: str
  split_on_hyphen: bool
  try_without_trimming: bool
  try_without_splitting: bool
  # use this weight for words consisting only of trim_symbols
  # only relevant if trim_symbols is not empty
  default_weight: Optional[float]


def word2pronunciation(word: Word, lookup: LookupMethod, options: Options) -> Pronunciations:
  assert isinstance(word, str)
  assert isinstance(options, Options)

  if word == "":
    return OrderedDict()

  if len(options.trim_symbols) > 0 and options.try_without_trimming:
    lookup_result = lookup(word)

    if len(lookup_result) > 0:
      return lookup_result

  if len(options.trim_symbols) > 0:
    trim_beginning, word_core, trim_end = separate_symbols(word, options.trim_symbols)
    contains_only_punctuation = word_core == ""
    if contains_only_punctuation:
      assert trim_end == ""
      assert trim_beginning == word
      pronunciation = tuple(word)
      result = OrderedDict((
        (pronunciation, options.default_weight),
      ))
      return result
  else:
    trim_beginning = ""
    word_core = word
    trim_end = ""

  if options.split_on_hyphen and options.try_without_splitting:
    lookup_result = lookup(word_core)

    if len(lookup_result) > 0:
      result = join_begin_and_end(lookup_result, trim_beginning, trim_end)
      return result

  if options.split_on_hyphen:
    words = word_core.split(HYPHEN)
    resulting_pronunciations = []
    for w in words:
      if w == "":
        resulting_pronunciations.append(None)
      else:
        lookup_result = lookup(w)
        if len(lookup_result) == 0:
          # or add None for ignoring that no result was returned
          return OrderedDict()
        resulting_pronunciations.append(lookup_result)
    lookup_result = merge_pronunciations(
      resulting_pronunciations, options.default_weight)
  else:
    lookup_result = lookup(word_core)

  result = join_begin_and_end(lookup_result, trim_beginning, trim_end)
  return result


def join_begin_and_end(pronunciations: Pronunciations, beginning: str, end: str) -> Pronunciations:
  if beginning == "" and end == "":
    return pronunciations

  result = OrderedDict()
  beginning_list = list(beginning)
  ending_list = list(end)
  for pronunciation, weight in pronunciations.items():
    new_pronunciation = beginning_list + list(pronunciation) + ending_list
    new_pronunciation = tuple(new_pronunciation)
    result[new_pronunciation] = weight
  return result


def get_matrix(pronunciations: List[Optional[Pronunciations]]) -> List[List[Optional[Tuple[Pronunciation, Weight]]]]:
  result: List[List[Optional[Tuple[Pronunciation, Weight]]]] = []
  for p in pronunciations:
    if p is None:
      if len(result) == 0:
        result = [[None]]
      else:
        for entry in result:
          entry.append(None)
    else:
      if len(result) == 0:
        result = [[x] for x in p.items()]
      else:
        new_res = []
        for entry in result:
          for p2, w2 in p.items():
            new_entry = entry + [(p2, w2)]
            new_res.append(new_entry)
        result = new_res
  return result


def get_weights(matrix: List[List[Optional[Tuple[Pronunciation, Weight]]]]) -> Generator[Optional[Weight], None, None]:
  for row in matrix:
    last_val = None
    for col in row:
      if col is None:
        continue
      p, w = col
      assert p is not None
      assert w is not None
      if last_val is None:
        last_val = w
      else:
        last_val *= w
    yield last_val


def get_pronunciations(matrix: List[List[Optional[Tuple[Pronunciation, Weight]]]]) -> Generator[List[Pronunciation], None, None]:
  for row in matrix:
    pronunciations = []
    for col in row:
      if col is None:
        pronunciations.append(tuple())
        continue
      p, w = col
      assert p is not None
      assert w is not None
      pronunciations.append(p)
    yield pronunciations


def merge_pronunciations(parts: List[Optional[Pronunciations]], default_weight: Optional[Weight]) -> Pronunciations:
  # TODO convert weights first to propabilities
  result = OrderedDict()
  matrix = get_matrix(parts)
  for pronunciation_parts, weight in zip(get_pronunciations(matrix), get_weights(matrix)):
    joined_parts = tuple(symbols_join(pronunciation_parts, HYPHEN))
    if len(joined_parts) == 0:
      continue
    if weight is None:
      assert default_weight is not None
      assert default_weight > 0
      weight = default_weight
    result[joined_parts] = weight
  return result
