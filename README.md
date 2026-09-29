# bunches

| | |
| --- | --- |
| Version | [![PyPI Latest Release](https://img.shields.io/pypi/v/bunches.svg?style=for-the-badge&color=steelblue&label=PyPI&logo=PyPI&logoColor=yellow)](https://pypi.org/project/bunches/) [![GitHub Latest Release](https://img.shields.io/github/v/tag/WithPrecedent/bunches?style=for-the-badge&color=navy&label=GitHub&logo=github)](https://github.com/WithPrecedent/bunches/releases)
| Status | [![Build Status](https://img.shields.io/github/actions/workflow/status/WithPrecedent/bunches/ci.yml?branch=main&style=for-the-badge&color=cadetblue&label=Tests&logo=pytest)](https://github.com/WithPrecedent/bunches/actions/workflows/ci.yml?query=branch%3Amain) [![Development Status](https://img.shields.io/badge/Development-Active-seagreen?style=for-the-badge&logo=git)](https://www.repostatus.org/#active) [![Project Stability](https://img.shields.io/pypi/status/bunches?style=for-the-badge&logo=pypi&label=Stability&logoColor=yellow)](https://pypi.org/project/bunches/)
| Documentation | [![Hosted By](https://img.shields.io/badge/Hosted_by-Github_Pages-blue?style=for-the-badge&color=navy&logo=github)](https://WithPrecedent.github.io/bunches)
| Tools | [![Documentation](https://img.shields.io/badge/MkDocs-magenta?style=for-the-badge&color=deepskyblue&logo=markdown&labelColor=gray)](https://squidfunk.github.io/mkdocs-material/) [![Linter](https://img.shields.io/endpoint?style=for-the-badge&url=https://raw.githubusercontent.com/charliermarsh/Ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/Ruff) [![Dependency Manager](https://img.shields.io/badge/uv-mediumpurple?style=for-the-badge&logo=uv&labelColor=gray&logoColor=white)](https://docs.astral.sh/uv/) [![Pre-commit](https://img.shields.io/badge/pre--commit-darkolivegreen?style=for-the-badge&logo=pre-commit&logoColor=white&labelColor=gray)](https://github.com/TezRomacH/python-package-template/blob/master/.pre-commit-config.yaml) [![CI](https://img.shields.io/badge/GitHub_Actions-navy?style=for-the-badge&logo=githubactions&labelColor=gray&logoColor=white)](https://github.com/features/actions) [![Editor Settings](https://img.shields.io/badge/Editor_Config-paleturquoise?style=for-the-badge&logo=editorconfig&labelColor=gray)](https://editorconfig.org/) [![Repository Template](https://img.shields.io/badge/snickerdoodle-bisque?style=for-the-badge&logo=cookiecutter&labelColor=gray)](https://www.github.com/WithPrecedent/snickerdoodle) [![Dependency Maintainer](https://img.shields.io/badge/dependabot-navy?style=for-the-badge&logo=dependabot&logoColor=white&labelColor=gray)](https://github.com/dependabot)
| Compatibility | [![Compatible Python Versions](https://img.shields.io/pypi/pyversions/bunches?style=for-the-badge&color=steelblue&label=Python&logo=python&logoColor=yellow)](https://pypi.python.org/pypi/bunches/) [![Linux](https://img.shields.io/badge/Linux-lightseagreen?style=for-the-badge&logo=linux&labelColor=gray&logoColor=white)](https://www.linux.org/) [![MacOS](https://img.shields.io/badge/MacOS-snow?style=for-the-badge&logo=apple&labelColor=gray)](https://www.apple.com/macos/) [![Windows](https://img.shields.io/badge/windows-blue?style=for-the-badge&logo=Windows&labelColor=gray&color=orangered)](https://www.microsoft.com/en-us/windows?r=1)
| Stats | [![PyPI Download Rate (per month)](https://img.shields.io/pypi/dm/bunches?style=for-the-badge&color=steelblue&label=Downloads%20💾&logo=pypi&logoColor=yellow)](https://pypi.org/project/bunches) [![GitHub Stars](https://img.shields.io/github/stars/WithPrecedent/bunches?style=for-the-badge&color=navy&label=Stars%20⭐&logo=github)](https://github.com/WithPrecedent/bunches/stargazers) [![GitHub Contributors](https://img.shields.io/github/contributors/WithPrecedent/bunches?style=for-the-badge&color=navy&label=Contributors%20🙋&logo=github)](https://github.com/WithPrecedent/bunches/graphs/contributors) [![GitHub Issues](https://img.shields.io/github/issues/WithPrecedent/bunches?style=for-the-badge&color=navy&label=Issues%20📘&logo=github)](https://github.com/WithPrecedent/bunches/graphs/contributors) [![GitHub Forks](https://img.shields.io/github/forks/WithPrecedent/bunches?style=for-the-badge&color=navy&label=Forks%20🍴&logo=github)](https://github.com/WithPrecedent/bunches/forks)
| | |

-----

## What is bunches?

`bunches` provides drop-in replacements for Python's built-in `dict` and `list` that add a consistent set of extra tools. Every class in the package:

* stores its data in a plain Python collection in the `contents` attribute, so you can always drop back to the built-in type;
* has an `add` method, the default way to put data in the collection;
* has a `delete` method, the default way to remove data (it is also what `del collection[item]` calls);
* has a `subset` method that returns a new collection containing only some of the data;
* supports `+` (returns a new collection with an item added) and `+=` (adds the item in place), both of which use `add`.

The package is fully typed, has no dependencies, and supports Python 3.11 and later.

## Why use bunches?

The built-in collections are excellent, but they leave you to re-implement the same conveniences whenever you build a registry, a set of options, or an ordered group of named items. `bunches` supplies those conveniences once: wildcard lookups, keys inferred from the items you store, layered dictionaries, and lists that can be searched by name.

## Classes

### Mappings

* `Dictionary`: drop-in replacement for a python `dict` with an `add` method for a default mechanism of adding data, a `delete` method for a default mechanism of deleting data, and a `subset` method for returning a subset of the key/value pairs in a new `Dictionary`. Its `keys`, `values` and `items` methods return `tuple`s and it has `defaultdict`-like behavior when using `get`.
* `Catalog`: wildcard-accepting dict which is intended for storing different options and strategies. It recognizes the special keys `all`, `default` and `none` and returns lists of matches if a list of keys is provided.
* `ChainDict`: a `Dictionary` that stores several dictionaries and searches them in order, like `collections.ChainMap`.
* `Repository`: a dictionary that automatically supplies key names for stored items. The `overwrite` argument determines if a unique key should always be created or whether entries may be overwritten.

### Sequences

* `Listing`: drop-in replacement for a python list with an `add` method for a default mechanism of adding data, a `delete` method for a default mechanism of deleting data, a `prepend` method, and a `subset` method for returning a subset of the items in a new `Listing`.
* `DictList`: iterable with both dict and list interfaces. Stored items must be hashable or have a `name` attribute.

## Getting started

### Requirements

`bunches` requires Python 3.11 or later and runs on Linux, macOS and Windows. It has no third-party dependencies.

### Installation

To install `bunches`, use `pip`:

```sh
pip install bunches
```

### Usage

#### Dictionary

A `Dictionary` works like a `dict`. Its `add` method updates the stored data, `subset` returns a new `Dictionary`, and `get` falls back on `default_factory` (a value or a callable) when a key is missing.

```python
from bunches import Dictionary

colors = Dictionary(contents={"red": 1, "green": 2}, default_factory=0)
colors.add({"blue": 3})
colors["blue"]  # 3
colors.get("purple")  # 0
colors.subset(include=["red", "blue"]).contents  # {'red': 1, 'blue': 3}
colors.subset(exclude="red").keys()  # ('green', 'blue')
del colors["green"]
colors.contents  # {'red': 1, 'blue': 3}
(colors + {"pink": 4}).contents  # {'red': 1, 'blue': 3, 'pink': 4}
colors.contents  # {'red': 1, 'blue': 3}
```

#### Catalog

A `Catalog` is meant for storing options. The `all`, `default` and `none` keys are special and a list of keys returns a list of values.

```python
from bunches import Catalog

models = Catalog(contents={"tree": "DecisionTree", "forest": "RandomForest"})
models["tree"]  # 'DecisionTree'
models[["tree", "forest"]]  # ['DecisionTree', 'RandomForest']
models["all"]  # ['DecisionTree', 'RandomForest']
models.default = "forest"
models["default"]  # 'RandomForest'
models["none"] is None  # True
```

#### ChainDict

A `ChainDict` searches its stored dictionaries in order and returns the first match. Set `return_first` to `False` to get every match.

```python
from bunches import ChainDict, Dictionary

chain = ChainDict(contents=[Dictionary({"a": 1}), Dictionary({"a": 2, "b": 3})])
chain["a"], chain["b"]  # (1, 3)
chain.return_first = False
chain["a"]  # [1, 2]
chain.new_child(Dictionary({"c": 4}))
chain.keys()  # ('c', 'a', 'a', 'b')
```

#### Repository

A `Repository` infers the key for each item added: the item itself if it is a `str`, its `name` attribute, or the snake-cased name of its class. Unless `overwrite` is `True`, a counter is appended to avoid overwriting existing items.

```python
from dataclasses import dataclass
from bunches import Repository


@dataclass
class Worker:
    name: str


class DataLoader:
    pass


repository = Repository()
repository.add(Worker("ann"))
repository.add(DataLoader())
repository.add(DataLoader())
repository.add(Worker("bob"), key="boss")
repository.keys()  # ('ann', 'data_loader', 'data_loader2', 'boss')
```

#### Listing

A `Listing` works like a `list`. `add` extends the list with a sequence and appends anything else, and `prepend` does the same at the beginning.

```python
from bunches import Listing

letters = Listing(contents=["b", "c"])
letters.add("d")
letters.add(["e", "f"])
letters.prepend("a")
letters.contents  # ['a', 'b', 'c', 'd', 'e', 'f']
letters.subset(include=["a", "b", "c"], exclude="b").contents  # ['a', 'c']
letters.delete(0)
letters[0]  # 'b'
```

#### DictList

A `DictList` is a `list` you can also search by name. Items are found by their `name` attribute or, if they have none, by their own value. Duplicate names are allowed; a `DictList` of the matches is returned.

```python
from bunches import DictList

workers = DictList(contents=[Worker("ann"), Worker("bob"), Worker("ann")])
workers.keys()  # ('ann', 'bob', 'ann')
workers["bob"]  # Worker(name='bob')
len(workers["ann"])  # 2
workers[1]  # Worker(name='bob')
workers.delete("ann")
workers.keys()  # ('bob',)
```

#### Choosing what `subset` returns

Every `subset` method has a `returns` argument. `'class'` (the default) returns a new instance of the same class, `'copy'` returns a deep copy of the instance (keeping its other settings) and `'simple'` returns the built-in type. To change the default for the whole package, use `bunches.settings.set_subset_return`.

```python
colors = Dictionary({"red": 1, "green": 2})
colors.subset(include="red", returns="simple")  # {'red': 1}
```

#### Naming items

`Repository` and `DictList` name items with a global function that you can replace using `bunches.settings.set_key_namer`.

```python
from bunches import settings

settings.set_key_namer(lambda item: str(item).upper())
Repository({"a": 1}).add("b")
DictList(["x", "y"]).keys()  # ('X', 'Y')
settings.set_key_namer(settings.utilities._namify)
```

## Contributing

Contributors are always welcome. Feel free to grab an [issue](https://www.github.com/WithPrecedent/bunches/issues) to work on or make a suggested improvement. If you wish to contribute, please read the [Contribution Guide](https://www.github.com/WithPrecedent/bunches/blob/main/CONTRIBUTING.md) and [Code of Conduct](https://www.github.com/WithPrecedent/bunches/blob/main/CODE_OF_CONDUCT.md).

## Similar Projects

* [`collections`](https://docs.python.org/3/library/collections.html) in the Python standard library provides `UserDict`, `UserList`, `ChainMap` and `defaultdict`, which inspired several of the classes in `bunches`.
* [`sortedcontainers`](https://grantjenks.com/docs/sortedcontainers/) provides sorted drop-in replacements for `list`, `dict` and `set`.

## Acknowledgments

I'd also like to extend a special thanks to [pawamoy](https://github.com/pawamoy) whose excellent `mkdocs` extensions and utilities are incorporated into `snickerdoodle`. Some of the scripts, documentation, configuration files, and other CI code were adapted from pawamoy's repositories.

I would also like to thank the University of Kansas School of Law for tolerating and supporting this law professor's coding efforts, an endeavor which is well outside the typical scholarly activities in the discipline.

## License

Use of this repository is authorized under the [Apache Software License 2.0](https://www.github.com/WithPrecedent/bunches/blob/main/LICENSE).
