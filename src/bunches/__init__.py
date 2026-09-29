"""Drop-in replacements for Python collections.

Contents:
    Bunch: abstract base class for the collections in the package.
    Dictionary: drop-in replacement for a `dict`.
    Catalog: wildcard and list-accepting `Dictionary`.
    ChainDict: `Dictionary` with the functionality of `collections.ChainMap`.
    Repository: `Dictionary` which infers the keys of the items added to it.
    Listing: drop-in replacement for a `list`.
    DictList: `list` with a `dict` interface.

"""

from __future__ import annotations

__version__ = "0.2.0"

__author__: str = "Corey Rayburn Yung"


from .base import Bunch
from .mappings import Catalog, ChainDict, Dictionary, Repository
from .sequences import DictList, Listing

__all__: list[str] = [
    "Bunch",
    "Catalog",
    "ChainDict",
    "DictList",
    "Dictionary",
    "Listing",
    "Repository",
]
