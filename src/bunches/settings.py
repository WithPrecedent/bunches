"""Settings for `bunches`.

Contents:


To Do:


"""
from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from . import utilities

if TYPE_CHECKING:
    from .kinds import SubsetReturns


_ALL_KEYS: list[Any] = ['all', 'All', ['all'], ['All']]
_DEFAULT_KEYS: list[Any] = [
    'default', 'defaults', 'Default', 'Defaults', ['default'], ['defaults'],
    ['Default'], ['Defaults']]
_KEY_NAMER: Callable[[object | type[Any]], str] = utilities._namify
_METHOD_NAMER: Callable[[object | type[Any]], str] = (
    lambda x: f'from_{utilities._namify(x)}')
_NONE_KEYS: list[Any] = ['none', 'None', ['none'], ['None']]
_SUBSET_RETURN: SubsetReturns = 'class'


def set_key_namer(namer: Callable[[object | type[Any]], str]) -> None:
    """Sets the global default function used to name items.

    Args:
        namer: function that returns a str name of any item passed.

    Raises:
        TypeError: if 'namer' is not callable.

    """
    if isinstance(namer, Callable):
        globals()['KEYER'] = namer
    else:
        raise TypeError('namer argument must be a callable')

def set_method_namer(namer: Callable[[object | type[Any]], str]) -> None:
    """Sets the global default function used to name factory methods.

    Args:
        namer (Callable[[object | Type[Any]], str]): function that returns a
            str name of any item passed.

    Raises:
        TypeError: if 'namer' is not callable.

    """
    if isinstance(namer, Callable):
        globals()['_METHOD_NAMER'] = namer
    else:
        raise TypeError('namer argument must be a callable')
