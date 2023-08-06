import random
from collections import OrderedDict
from typing import Any, List, Protocol, TypeVar

from pronunciation_dictionary_cli.cli import parse_args

t = str

print(t.__name__)

x1 = OrderedDict([("a", 1)])
x2 = OrderedDict([("a", 2)])
x3 = OrderedDict([("a", 1)])
print(x1 == x2)
print(x1 == x1)
print(x1 == x3)


T = TypeVar('T', bound='Other')


class Other:
  def copy(self: T) -> T:
    ...


class Bar(Protocol):
  def oogle(self, quz: List[int]) -> Any:
    ...


x = IPronunciationDictionary()
x = x.deserialize()


class XX(Other):
  pass


x = XX()
x.copy()
parse_args(['extract', '/tmp/test.dict', '/tmp/vocabulary.txt', '/tmp/out.dict'])


random.seed(1)
print(random.choice(["a", "b"]))

random.seed(1)
print(random.choice(["a", "b"]))

random.seed(1)
print(random.choice(["b", "a"]))

random.seed(1)
print(random.choice(["c", "d"]))

parse_args(["merge", "/tmp/out.dict", "/tmp/out.dict"])


print(".!abe?".replace("!.?", ""))
parse_args(['remove-symbols-from-pronunciations', '/tmp/test.dict', "-j", "1"])


parse_args(['create-from-dict', '/tmp/test.txt', '/tmp/out.dict',
           '/tmp/pronunciations.dict', '--ignore-case', "-j", "1"])
parse_args(["download", "cmu"])
