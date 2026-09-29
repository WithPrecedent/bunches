"""Settings for `bunches`.

Contents:
    set_key_namer: sets the global function used to name items.
    set_method_namer: sets the global function used to name factory methods.
    set_subset_return: sets the global default `returns` option for `subset`
        methods.

The module-level values (`_ALL_KEYS`, `_DEFAULT_KEYS`, `_NONE_KEYS`,
`_KEY_NAMER`, `_METHOD_NAMER`, and `_SUBSET_RETURN`) hold the package-wide
defaults. They are read at call time, so the `set_*` functions take effect
immediately for all `bunches` classes.

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
_KEY_NAMER: Callable[[object | type[Any]], str | None] = utilities._namify
_METHOD_NAMER: Callable[[object | type[Any]], str] = (
    lambda x: f'from_{utilities._namify(x)}')
_NONE_KEYS: list[Any] = ['none', 'None', ['none'], ['None']]
_SUBSET_RETURN: SubsetReturns = 'class'


def set_key_namer(namer: Callable[[object | type[Any]], str | None]) -> None:
    """Sets the global default function used to name items.

    Args:
        namer: function that returns a `str` name of any item passed.

    Raises:
        TypeError: if 'namer' is not callable.

    """
    if not callable(namer):
        raise TypeError('namer argument must be a callable')
    globals()['_KEY_NAMER'] = namer

def set_method_namer(namer: Callable[[object | type[Any]], str]) -> None:
    """Sets the global default function used to name factory methods.

    Args:
        namer: function that returns a `str` name of any item passed.

    Raises:
        TypeError: if 'namer' is not callable.

    """
    if not callable(namer):
        raise TypeError('namer argument must be a callable')
    globals()['_METHOD_NAMER'] = namer

def set_subset_return(returns: SubsetReturns) -> None:
    """Sets the global default for the `returns` argument of `subset` methods.

    Args:
        returns: whether `subset` methods return a new instance of the class
            ('class'), a deep copy of the instance ('copy') or the simple
            native Python type ('simple').

    Raises:
        ValueError: if 'returns' is not 'class', 'copy', or 'simple'.

    """
    if returns not in ('class', 'copy', 'simple'):
        message = 'returns argument must be "class", "copy", or "simple"'
        raise ValueError(message)
    globals()['_SUBSET_RETURN'] = returns
