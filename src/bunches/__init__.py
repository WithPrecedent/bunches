"""Drop-in replacements for Python collections"""

from __future__ import annotations

__version__ = '0.1.3'

__author__: str = 'Corey Rayburn Yung'


from .base import Bunch
from .mappings import Catalog, ChainDict, Dictionary, Repository
from .sequences import DictList, Listing

__all__: list[str] = [
    "Bunch",
    "Catalog",
    "ChainDict",
    "Dictionary",
    "DictList",
    "Listing",
    "Repository"]
