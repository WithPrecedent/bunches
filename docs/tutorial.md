# Tutorial

This tutorial walks through each class in `bunches`. Every example can be pasted into a Python 3.11+ session after installing the package:

```sh
pip install bunches
```

## The shared interface

All `bunches` classes derive from `bunches.Bunch`. They keep their data in a built-in collection in the `contents` attribute and share these methods:

| Member | Purpose |
| --- | --- |
| `add(item)` | The default way to put data in the collection. |
| `delete(item)` | The default way to remove data. Called by `del collection[item]`. |
| `subset(include, exclude, returns)` | Returns a new collection with only some of the data. |
| `collection + item` | Returns a *new* collection with `item` added using `add`. |
| `collection += item` | Adds `item` in place using `add`. |
| `contents` | The underlying `dict` or `list`. |

## `Dictionary`

```python
from bunches import Dictionary

colors = Dictionary(contents = {'red': 1, 'green': 2}, default_factory = 0)
colors.add({'blue': 3})
colors.subset(include = ['red', 'blue']).contents   # {'red': 1, 'blue': 3}
colors.get('purple')                                # 0 (default_factory)
colors.keys()                                       # ('red', 'green', 'blue')
```

`keys`, `values` and `items` return `tuple`s. `get` uses `default_factory` when a key is missing: it is called if it is callable and returned as-is otherwise. If neither a `default` argument nor a `default_factory` exists, `get` raises `KeyError`.

## `Catalog`

A `Catalog` stores options and understands wildcards:

```python
from bunches import Catalog

catalog = Catalog({'tree': 'DecisionTree', 'forest': 'RandomForest'})
catalog['all']                  # ['DecisionTree', 'RandomForest']
catalog[['tree', 'forest']]     # ['DecisionTree', 'RandomForest']
catalog.default = 'forest'
catalog['default']              # 'RandomForest'
catalog['none']                 # None
```

Set `always_return_list = True` to always receive a `list`, even for a single key.

## `ChainDict`

A `ChainDict` layers several dictionaries. Earlier dictionaries win:

```python
from bunches import ChainDict, Dictionary

settings = ChainDict([Dictionary({'debug': True}), Dictionary({'debug': False, 'name': 'app'})])
settings['debug']          # True
settings['name']           # 'app'
settings.return_first = False
settings['debug']          # [True, False]
```

Use `new_child` to put a new dictionary in front and `parents()` to get a `ChainDict` without the first dictionary.

## `Repository`

A `Repository` chooses the keys for you when you call `add`:

```python
from bunches import Repository

repository = Repository()
repository.add('apple')             # key: 'apple'
repository.add(object())            # key: 'object'
repository.add(object())            # key: 'object2'
repository.add(3.5, key = 'price')  # explicit key
```

Pass `overwrite = True` to replace an existing item with the same inferred key instead of adding a numeric suffix.

## `Listing`

```python
from bunches import Listing

letters = Listing(['b', 'c'])
letters.add('d')            # appends strings: ['b', 'c', 'd']
letters.add(['e', 'f'])     # extends with other sequences
letters.prepend('a')        # ['a', 'b', 'c', 'd', 'e', 'f']
letters.subset(include = ['a', 'b'], exclude = 'b').contents   # ['a']
```

## `DictList`

A `DictList` lets you look up list items by name. Duplicate names are allowed:

```python
from dataclasses import dataclass
from bunches import DictList

@dataclass
class Worker:
    name: str

team = DictList([Worker('ann'), Worker('bob'), Worker('ann')])
team['bob']         # Worker(name='bob')
team['ann']         # DictList of both 'ann' workers
team[0]             # Worker(name='ann') (int keys are indices)
team.keys()         # ('ann', 'bob', 'ann')
```

Because `int` values are treated as indices, avoid storing `int`s in a `DictList`.
