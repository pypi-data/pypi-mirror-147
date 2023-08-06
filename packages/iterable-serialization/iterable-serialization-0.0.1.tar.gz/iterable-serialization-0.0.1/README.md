# iterable-serialization

Serialization/deserialization of iterables of type `str`.

This package aims to be a better version of:

```python
serialized = "|".join(("a", "b", "c"))
print(serialized)
# a|b|c

deserialized = serialized.split("|")
print(deserialized)
# ['a', 'b', 'c']
```

It makes it possible to serialize/deserialize an iterable with occurring symbols as separator:

```python
serialized = serialize_iterable(("a", "b", "c"), "a")
print(serialized)
# aabac

deserialized = deserialize_iterable(serialized, "a")
print(list(deserialized))
# ['a', 'b', 'c']
```

With the version above, it would result in a wrong deserialization result:

```python
serialized = "a".join(("a", "b", "c"))
print(serialized)
# aabac

deserialized = serialized.split("a")
print(list(deserialized))
# ['', '', 'b', 'c']
```

## Installation

```sh
pipenv install -e git+https://github.com/stefantaubert/iterable-serialization.git@master#egg=iterable_serialization
```

## Usage

```python
from iterable_serialization import deserialize_iterable, serialize_iterable

serialized = serialize_iterable(("a", "b", "c"), "a")
print(serialized)
# aabac

deserialized = deserialize_iterable(serialized, "a")
print(list(deserialized))
# ['a', 'b', 'c']
```
