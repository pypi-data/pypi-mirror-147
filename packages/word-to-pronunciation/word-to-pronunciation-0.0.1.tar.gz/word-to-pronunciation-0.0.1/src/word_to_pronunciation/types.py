from typing import Callable

from pronunciation_dictionary import Pronunciations, Word

LookupMethod = Callable[[Word], Pronunciations]
