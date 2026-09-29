# Recipes

## A plugin registry

Use a `Repository` so plugins register themselves under an inferred name:

```python
from bunches import Repository

plugins = Repository(overwrite = True)

def register(cls):
    plugins.add(cls)
    return cls

@register
class CsvReader: ...

plugins.keys()          # ('csv_reader',)
```

## Layered configuration

Search command-line options, then a config file, then defaults:

```python
from bunches import ChainDict, Dictionary

config = ChainDict([
    Dictionary({'debug': True}),                       # command line
    Dictionary({'debug': False, 'path': '/tmp'}),      # config file
    Dictionary({'path': '.', 'retries': 3})])          # defaults

config['debug']     # True
config['path']      # '/tmp'
config['retries']   # 3
```

## Strategy options with a default

```python
from bunches import Catalog

sorters = Catalog(
    contents = {'quick': 'quicksort', 'merge': 'mergesort'},
    default = 'merge')

sorters['default']      # 'mergesort'
sorters['all']          # ['quicksort', 'mergesort']
```

## Ordered pipeline steps you can look up by name

```python
from dataclasses import dataclass
from bunches import DictList

@dataclass
class Step:
    name: str

pipeline = DictList([Step('load'), Step('clean'), Step('save')])
pipeline['clean']       # Step(name='clean')
pipeline.insert(1, Step('validate'))
pipeline.keys()         # ('load', 'validate', 'clean', 'save')
```

## Getting back to built-in types

Every `Bunch` keeps plain data in `contents`, and `subset` can return it directly:

```python
from bunches import Listing

Listing([1, 2, 3]).subset(exclude = 2, returns = 'simple')   # [1, 3]
```
