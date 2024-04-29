"""System and functions for inferring object and class names.

Contents:


To Do:


"""
from __future__ import annotations

import copy
import inspect
import re
from collections.abc import Collection, Iterable, Sequence
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .kinds import GenericDict, SubsetReturns


def _capitalify(item: str) -> str:
    """Converts a snake case `str` to capital case.

    Args:
        item: `str` to convert.

    Returns:
        'item' converted to capital case.

    """
    return item.replace('_', ' ').title().replace(' ', '')

def _is_sequence(item: Any) -> bool:
    """Returns if 'item' is a sequence but not a `str`.

    Args:
        item: object to examine.

    Returns:
        If 'item' is a sequence but not a `str`.

    """
    if not inspect.isclass(item):
        item = item.__class__
    return issubclass(item, Sequence) and not issubclass(item, str)

def _iterify(item: Any) -> Iterable:
    """Returns `item` as an iterable, but does not iterate `str` types.

    Args:
        item: item to turn into an iterable.

    Returns:
        Iterable of `item`. A `str` type will be stored as a single item in an
            iterable wrapper.

    """
    if item is None:
        return iter(())
    elif isinstance(item, str | bytes):
        return iter([item])
    else:
        try:
            return iter(item)
        except TypeError:
            return iter((item,))

def _namify(item: Any, /, default: str | None = None) -> str | None:
    """Returns `str` name representation of 'item'.

    Args:
        item: item to determine a `str` name.
        default: default name to return if other methods at name creation fail.

    Returns:
        str: a name representation of 'item.'

    """
    if isinstance(item, str):
        return item
    elif (
        hasattr(item, 'name')
        and not inspect.isclass(item)
        and isinstance(item.name, str)):
        return item.name
    else:
        try:
            return _snakify(item.__name__)
        except AttributeError:
            if item.__class__.__name__ is not None:
                return _snakify(item.__class__.__name__)
            else:
                return default

def _return_subset(
    subset: Collection,
    existing: Collection,
    returns: SubsetReturns) -> Collection:
    """Returns a subset of an item.

    Args:
        subset: native Python subset of data from a `Collection`.
        existing: a subclasss instance of `Collection`.
        returns: the type to be be returned by the function.

    Returns:
        A `Collection` with a `subset` of data.

    """
    if returns == "class":
        return existing.__class__(subset)
    elif returns == "copy":
        new_collection = copy.deepcopy(existing)
        new_collection.contents = subset
        return new_collection
    elif returns == "simple":
        return subset
    else:
        message = 'returns argument must be "class", "copy", or "simple"'
        raise ValueError(message)

def _snakify(item: str) -> str:
    """Converts a capitalized `str` to snake case.

    Args:
        item: `str`/. to convert.

    Returns:
        str: 'item' converted to snake case.

    """
    item = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', item)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', item).lower()

def _uniquify(
    key: str,
    dictionary: GenericDict,
    index: int | None = 1) -> str:
    """Creates a unique key name to avoid overwriting an item in 'dictionary'.

    The function is 1-indexed so that the first attempt to avoid a duplicate
    will be: "old_name2".

    Args:
        key: name of key to test.
        dictionary: `dict` for which a unique key name is sought.
        index: current index number for suffix. Defaults to 1.

    Returns:
        str: unique key name for 'dictionary'.

    """
    if key not in dictionary:
        return key
    counter = index
    while True:
        counter += 1
        if counter > 2:  # noqa: PLR2004
            key = key.removesuffix(str(counter - 1))
        key = ''.join([key, str(counter)])
        if key not in dictionary:
            return key
