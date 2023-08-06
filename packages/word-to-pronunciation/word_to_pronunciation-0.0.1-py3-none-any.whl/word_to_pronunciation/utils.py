import re
from typing import Generator, List, Optional, Tuple

from pronunciation_dictionary import Pronunciation, Symbol, Word


def symbols_join(list_of_pronunciations: List[Pronunciation], join_symbol: Optional[Symbol]) -> Generator[Symbol, None, None]:
  for i, word in enumerate(list_of_pronunciations):
    yield from word
    is_last_word = i == len(list_of_pronunciations) - 1
    if not is_last_word and join_symbol is not None and len(join_symbol) > 0:
      yield join_symbol


def separate_symbols(word: Word, symbols: str) -> Tuple[str, Word, str]:
  assert isinstance(word, str)
  assert isinstance(symbols, str)
  if symbols == "":
    return "", word, ""
  symbols_esc = re.escape(symbols)
  pattern = re.compile(rf"([{symbols_esc}]*)(.*)")
  res1 = re.match(pattern, word)
  assert res1 is not None
  start = res1.group(1)
  middle_tmp = res1.group(2)
  res2 = re.match(pattern, middle_tmp[::-1])
  assert res2 is not None
  middle = res2.group(2)[::-1]
  end = res2.group(1)[::-1]
  return start, middle, end
