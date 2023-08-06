from collections import OrderedDict
from functools import partial
from logging import getLogger
from typing import Dict, Optional

from pronunciation_dictionary import Pronunciations, Word

from word_to_pronunciation.core import Options, word2pronunciation
from word_to_pronunciation.types import LookupMethod


def __validate_options(options: Options) -> Optional[str]:
  if not isinstance(options.trim_symbols, str):
    return "Property 'trim_symbols': Value needs to be of type 'str'!"
  if not isinstance(options.split_on_hyphen, bool):
    return "Property 'split_on_hyphen': Value needs to be of type 'bool'!"
  if not isinstance(options.try_without_trimming, bool):
    return "Property 'try_without_trimming': Value needs to be of type 'bool'!"
  if not isinstance(options.try_without_splitting, bool):
    return "Property 'try_without_splitting': Value needs to be of type 'bool'!"
  if len(options.trim_symbols) > 0 and options.default_weight is None:
    return "Property 'default_weight': Value needs to be set if any 'trim_symbols' were defined!"
  if options.default_weight is not None:
    if not (isinstance(options.default_weight, float) or isinstance(options.default_weight, int)):
      return "Property 'default_weight': Value needs to be of type 'int' or 'float'!"
    if not options.default_weight > 0:
      return "Property 'default_weight': Value needs to be greater than zero!"

  return None


def get_pronunciations_from_word(word: Word, lookup: LookupMethod, options: Options) -> Pronunciations:
  if not isinstance(word, str):
    raise ValueError("Parameter 'word': Value needs to be of type 'str'!")
  if not callable(lookup):
    raise ValueError("Parameter 'lookup': Value needs to be callable!")
  if msg := __validate_options(options):
    raise ValueError(f"Parameter 'options': {msg}")

  internal_lookup_method = partial(
    lookup_with_check,
    lookup=lookup,
  )

  return word2pronunciation(word, internal_lookup_method, options)


def get_cached_lookup(lookup: LookupMethod, cache: Dict[Word, Pronunciations]) -> LookupMethod:
  if not callable(lookup):
    raise ValueError("Parameter 'lookup': Value needs to be callable!")
  if not isinstance(cache, dict):
    raise ValueError("Parameter 'cache': Value needs to be of type 'dict'!")

  result = partial(
    lookup_cached,
    lookup=lookup,
    cache=cache,
  )
  return result


def lookup_cached(word: Word, lookup: LookupMethod, cache: Dict[Word, Pronunciations]) -> Pronunciations:
  if word in cache:
    return cache[word]
  else:
    result = lookup(word)
    cache[word] = result
    return result


def lookup_with_check(word: Word, lookup: LookupMethod) -> Pronunciations:
  logger = getLogger(__name__)
  try:
    result = lookup(word)
  except Exception as ex:
    logger.warning("Lookup method raised an exception!")
    logger.debug(ex)
    return OrderedDict()

  if not isinstance(result, OrderedDict):
    logger.warning("Lookup method returned an invalid pronunciation!")
    return OrderedDict()

  for k, v in result.items():
    if not isinstance(k, tuple) or not len(k) > 0:
      logger.warning("Lookup method returned an invalid pronunciation!")
      logger.debug(result)
      return OrderedDict()
    if not (isinstance(v, float) or isinstance(v, int)) and not v > 0:
      logger.warning("Lookup method returned an invalid pronunciation weight!")
      logger.debug(result)
      return OrderedDict()

  return result
