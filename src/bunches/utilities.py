"""Functions for inferring names, iterating, and building subsets.

Contents:
    _capitalify: converts a snake case `str` to capital case.
    _is_sequence: returns whether an item is a sequence, but not `str` or
        `bytes`.
    _iterify: returns an item as an iterator without iterating `str` types.
    _namify: infers a `str` name for an object or class.
    _return_subset: builds the return value of `subset` methods.
    _snakify: converts a capitalized `str` to snake case.
    _uniquify: creates a key that is not yet in a mapping.

"""

from __future__ import annotations

import copy
import inspect
import re
from collections.abc import Collection, Iterator, Sequence
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
    return item.replace("_", " ").title().replace(" ", "")


def _is_sequence(item: Any) -> bool:
    """Returns if 'item' is a sequence but not a `str` or `bytes`.

    Args:
        item: object or class to examine.

    Returns:
        If 'item' is a sequence but not a `str` or `bytes`.

    """
    if not inspect.isclass(item):
        item = item.__class__
    return issubclass(item, Sequence) and not issubclass(item, str | bytes)


def _iterify(item: Any) -> Iterator[Any]:
    """Returns `item` as an iterator, but does not iterate `str` types.

    Args:
        item: item to turn into an iterator.

    Returns:
        Iterator of `item`. `None` becomes an empty iterator. A `str` or `bytes`
            type (or any non-iterable) is wrapped so that it is returned as a
            single item.

    """
    if item is None:
        return iter(())
    if isinstance(item, str | bytes):
        return iter([item])
    try:
        return iter(item)
    except TypeError:
        return iter((item,))


def _namify(item: Any, /, default: str | None = None) -> str | None:
    """Returns `str` name representation of 'item'.

    The name is, in order of preference: 'item' itself if it is a `str`, the
    `name` attribute of an instance (if it is a `str`), the snake-cased
    `__name__` of a class or function, or the snake-cased name of the class of
    'item'.

    Args:
        item: item to determine a `str` name.
        default: name to return if no name can be derived. Defaults to `None`.

    Returns:
        A name representation of 'item' or 'default'.

    """
    if isinstance(item, str):
        return item
    if (
        hasattr(item, "name")
        and not inspect.isclass(item)
        and isinstance(item.name, str)
    ):
        return item.name
    name = getattr(item, "__name__", None)
    if not isinstance(name, str):
        name = getattr(item.__class__, "__name__", None)
    return _snakify(name) if isinstance(name, str) and name else default


def _return_subset(
    subset: Collection, existing: Collection, returns: SubsetReturns
) -> Collection:
    """Returns a subset of an item.

    Args:
        subset: native Python subset of data from a `Collection`.
        existing: a subclass instance of `Collection`.
        returns: whether to return a new instance of the class of 'existing'
            ('class'), a deep copy of 'existing' with 'subset' as its
            `contents` ('copy'), or 'subset' itself ('simple').

    Raises:
        ValueError: if 'returns' is not 'class', 'copy', or 'simple'.

    Returns:
        A `Collection` with a `subset` of data.

    """
    if returns == "class":
        return existing.__class__(subset)  # type: ignore[call-arg]
    if returns == "copy":
        new_collection = copy.deepcopy(existing)
        new_collection.contents = subset  # type: ignore[attr-defined]
        return new_collection
    if returns == "simple":
        return subset
    message = 'returns argument must be "class", "copy", or "simple"'
    raise ValueError(message)


def _snakify(item: str) -> str:
    """Converts a capitalized `str` to snake case.

    Args:
        item: `str` to convert.

    Returns:
        'item' converted to snake case.

    """
    item = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", item)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", item).lower()


def _uniquify(key: str, dictionary: GenericDict, index: int = 1) -> str:
    """Creates a unique key name to avoid overwriting an item in 'dictionary'.

    The function is 1-indexed so that the first attempt to avoid a duplicate
    will be: "old_name2".

    Args:
        key: name of key to test.
        dictionary: `dict` for which a unique key name is sought.
        index: starting number for the suffix counter. Defaults to 1.

    Returns:
        A key name that is not in 'dictionary'.

    """
    if key not in dictionary:
        return key
    counter = index
    while True:
        counter += 1
        if counter > 2:  # noqa: PLR2004
            key = key.removesuffix(str(counter - 1))
        key = "".join([key, str(counter)])
        if key not in dictionary:
            return key
