"""Tests for `bunches.base`."""

from __future__ import annotations

import copy
import dataclasses
from typing import Any

import pytest

from bunches import (
    Bunch,
    Catalog,
    ChainDict,
    DictList,
    Dictionary,
    Listing,
    Repository,
    settings,
)


@dataclasses.dataclass
class MinimalBunch(Bunch):
    """Smallest concrete `Bunch` (a list wrapper) for testing base behavior."""

    contents: list[Any] = dataclasses.field(default_factory = list)

    def add(self, item: Any) -> None:
        """Appends `item`.

        Args:
            item: item to append to `contents`.

        """
        self.contents.append(item)

    def delete(self, item: int) -> None:
        """Deletes the item at index `item`.

        Args:
            item: index of the item to delete.

        """
        del self.contents[item]

    def subset(
            self,
            include: Any = None,
            exclude: Any = None,
            returns: Any = None) -> Any:
        """Returns a new instance with `include` items.

        Args:
            include: items to include.
            exclude: ignored.
            returns: ignored.

        Returns:
            A new instance with the items in `include`.

        """
        return self.__class__([i for i in self.contents if i in include])

    def __contains__(self, item: object) -> bool:
        """Returns if `item` is in `contents`.

        Args:
            item: item to look for.

        Returns:
            Whether `item` is in `contents`.

        """
        return item in self.contents


def test_bunch_is_abstract() -> None:
    """Tests that `Bunch` cannot be instantiated without required methods."""
    with pytest.raises(TypeError):
        Bunch([1, 2])  # type: ignore[abstract]

    @dataclasses.dataclass
    class NoSubset(Bunch):
        """`Bunch` without the required `subset` method."""

        contents: list[Any] = dataclasses.field(default_factory = list)

        def add(self, item: Any) -> None:
            """Does nothing.

            Args:
                item: ignored.

            """

        def delete(self, item: Any) -> None:
            """Does nothing.

            Args:
                item: ignored.

            """

        def __contains__(self, item: object) -> bool:
            """Returns `False`.

            Args:
                item: ignored.

            Returns:
                `False`.

            """
            return False

    with pytest.raises(TypeError):
        NoSubset()  # type: ignore[abstract]


def test_collection_dunders() -> None:
    """Tests `__iter__`, `__len__`, and `__contains__`."""
    bunch = MinimalBunch([1, 2, 3])
    assert list(bunch) == [1, 2, 3]
    assert len(bunch) == 3
    assert 2 in bunch
    assert 4 not in bunch


def test_add_operators() -> None:
    """Tests `__add__` (copies) and `__iadd__` (in place)."""
    bunch = MinimalBunch([1])
    combined = bunch + 2
    assert combined.contents == [1, 2]
    assert bunch.contents == [1]
    assert combined is not bunch
    same = bunch
    bunch += 3
    assert bunch is same
    assert same.contents == [1, 3]


def test_delitem() -> None:
    """Tests `__delitem__`, which calls `delete`."""
    bunch = MinimalBunch([1, 2, 3])
    del bunch[0]
    assert bunch.contents == [2, 3]


def test_resolve_returns() -> None:
    """Tests `_resolve_returns`."""
    bunch = MinimalBunch()
    assert bunch._resolve_returns(None) == 'class'
    assert bunch._resolve_returns('copy') == 'copy'
    settings.set_subset_return('simple')
    assert bunch._resolve_returns(None) == 'simple'
    assert bunch._resolve_returns('class') == 'class'


def test_concrete_subclasses_are_bunches() -> None:
    """Tests that package classes are `Bunch` instances."""
    assert isinstance(Dictionary(), Bunch)
    assert isinstance(Listing(), Bunch)


@pytest.mark.parametrize(('instance', 'other'), [
    (Dictionary({'a': [1]}), {'b': [2]}),
    (Catalog({'a': [1]}), {'b': [2]}),
    (ChainDict([Dictionary({'a': [1]})]), {'b': [2]}),
    (Repository({'a': [1]}), [2]),
    (Listing([[1]]), [[2]]),
    (DictList(['a']), ['b'])])
def test_add_operators_all_classes(instance: Bunch, other: Any) -> None:
    """Tests that `+` copies and `+=` modifies in place for every class.

    Args:
        instance: instance of a `bunches` class.
        other: item to add to `instance`.

    """
    original = copy.deepcopy(instance)
    combined = instance + other
    assert type(combined) is type(instance)
    assert instance == original
    assert combined != original
    same = instance
    instance += other
    assert instance is same
    assert instance == combined
