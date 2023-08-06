from typing import Iterable, Optional


def serialize_iterable(iterable: Iterable[str], split_symbol: Optional[str] = None) -> str:
  if not isinstance(iterable, Iterable):
    raise ValueError("Parameter 'iterable': Value is not an Iterable!")
  if split_symbol is None:
    split_symbol = ""
  if not isinstance(split_symbol, str):
    raise ValueError("Parameter 'split_symbol': Value needs to be of type 'str'!")
  if not len(split_symbol) <= 1:
    raise ValueError("Parameter 'split_symbol': Value needs be at maximum one character!")
  result = ""
  is_first = True
  for item in iterable:
    if not isinstance(item, str):
      raise ValueError(
        f"Iterated item '{item}': Value could not be serialized because it is not of type 'str'!")
    if item == "":
      raise ValueError(
        f"Iterated item '{item}': Value is empty and therefore can not be serialized!")
    if split_symbol != "" and split_symbol in item and item != split_symbol:
      raise ValueError(
        f"Iterated item '{item}': Value could not be serialized because it contains the split_symbol!")
    if is_first:
      result = item
      is_first = False
    else:
      result = f"{result}{split_symbol}{item}"
  return result


def deserialize_iterable(serialized_iterable: str, split_symbol: Optional[str] = None) -> Iterable[str]:
  if not isinstance(serialized_iterable, str):
    raise ValueError("Parameter 'serialized_iterable': Value needs to be of type 'str'!")
  if split_symbol is None or split_symbol == "":
    yield from serialized_iterable
    return
    yield
  if not isinstance(split_symbol, str):
    raise ValueError("Parameter 'split_symbol': Value needs to be of type 'str'!")
  if not len(split_symbol) == 1:
    raise ValueError("Parameter 'split_symbol': Value needs to be exactly one character!")
  if serialized_iterable == "":
    return
    yield
  symbol = ""
  no_of_subsequent_split_symbols = 1
  last_char_was_non_split_symbol = False
  yield_subsequent_split_symbol = None
  for char in serialized_iterable:
    if char == split_symbol:
      no_of_subsequent_split_symbols += 1
      last_char_was_non_split_symbol = False
      if symbol == "":
        if yield_subsequent_split_symbol is None:
          yield char
          yield_subsequent_split_symbol = False
        elif yield_subsequent_split_symbol:
          yield char
          yield_subsequent_split_symbol = False
        else:
          yield_subsequent_split_symbol = True
      else:
        yield symbol
        symbol = ""
        yield_subsequent_split_symbol = True
    else:
      if no_of_subsequent_split_symbols % 2 == 0 and not last_char_was_non_split_symbol:
        raise ValueError(
          "Parameter 'serialized_iterable': Value can not be deserialized because the split_symbol occur subsequently on an even count!")
      no_of_subsequent_split_symbols = 0
      last_char_was_non_split_symbol = True
      symbol += char
  if not no_of_subsequent_split_symbols % 2 == 0:
    raise ValueError(
      "Parameter 'serialized_iterable': Value can not be deserialized because the split_symbol occur subsequently on an even count!")
  if symbol != "":
    yield symbol
