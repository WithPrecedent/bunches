# Advanced User Guide

## Choosing what `subset` returns

Each `subset` method has a `returns` argument:

| Value | Result |
| --- | --- |
| `'class'` | A new instance of the same class built from the subset. Other attributes (for example `default_factory`) take their default values. |
| `'copy'` | A deep copy of the instance whose `contents` are the subset. All other attributes are kept. |
| `'simple'` | The subset as the built-in type (`dict` or `list`; a `list` of `Dictionary` instances for `ChainDict`). |

When `returns` is `None` (the default), `bunches.settings.set_subset_return` determines the value:

```python
from bunches import Dictionary, settings

settings.set_subset_return('simple')
Dictionary({'a': 1, 'b': 2}).subset(include = 'a')   # {'a': 1}
```

## Changing how items are named

`Repository` and `DictList` name items using the function stored in `bunches.settings`. By default, an item's name is (in order of preference): the item if it is a `str`, its `name` attribute if that is a `str`, or the snake-cased name of its class or function. Replace the function globally with `set_key_namer`:

```python
from bunches import Repository, settings

settings.set_key_namer(lambda item: type(item).__name__)
```

To change naming for one class only, subclass and override `_get_name`:

```python
from bunches import Repository

class TypeRepository(Repository):
    def _get_name(self, item):
        return type(item).__name__
```

## Writing your own `Bunch`

A subclass of `bunches.Bunch` must be a `dataclass` with a `contents` field and implement `add`, `delete`, `subset` and `__contains__`. `__iter__` and `__len__` are provided, and `+`, `+=` and `del` work automatically:

```python
import dataclasses
from bunches import Bunch

@dataclasses.dataclass
class Stack(Bunch):
    contents: list = dataclasses.field(default_factory = list)

    def add(self, item):
        self.contents.append(item)

    def delete(self, item):
        del self.contents[item]

    def subset(self, include = None, exclude = None, returns = None):
        return self.__class__([i for i in self.contents if i in include])

    def __contains__(self, item):
        return item in self.contents
```

## Notes on behavior

* `Dictionary`, `Catalog`, `ChainDict` and `Repository` are `MutableMapping`s; `Listing` and `DictList` are `MutableSequence`s. All inherited methods (`update`, `pop`, `extend`, `reverse`, ...) work on `contents`.
* `+` never modifies the original instance; `+=` always does.
* `ChainDict` iteration, `len` and `keys` include a key once for every stored mapping that has it.
* `Catalog.delete` removes nothing if any key requested is missing.
* `DictList.delete` with a name that matches nothing raises `KeyError`.
