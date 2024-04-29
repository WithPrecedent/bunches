"""Base class for extensible, flexible, lightweight collection types.

Contents:
    Bunch (Collection, abc.ABC): base class for collections in `bunches`. It
        requires subclasses to have `add`, `delete`, and `subset` methods.

To Do:


"""
from __future__ import annotations

import abc
import dataclasses
from collections.abc import Collection, Hashable, Iterator
from typing import TYPE_CHECKING, Any, Self

from . import settings

if TYPE_CHECKING:
    from .kinds import SubsetReturns


@dataclasses.dataclass
class Bunch(Collection, abc.ABC):
    """Base for general `bunches` collections.

    A Bunch differs from a general python Collection in 5 ways:
        1) It must include an `add` method which provides the default mechanism
            for adding new items to the collection. `add` allows a subclass to
            designate the preferred method of adding to the collections`s stored
            data without replacing other access methods.
        2) It must include a `delete` method which provides the default
            mechanism for deleting items in the collection. `delete` is called
            by the `__delitem__` dunder method to delete stored items.
        3) A subclass must include a `subset` method with optional `include` and
            `exclude` parameters for returning a subset of the Bunch subclass.
        4) It supports the '+' operator being used to join a Bunch subclass
            instance of the same python type (mapping, sequence, tuple, etc.).
            The '+' operator calls the Bunch subclass `add` method to implement
            how the added item(s) is/are added to the Bunch subclass instance.
        5) It offers an accessible `contents` attribute that contains the native
            Python type for the `Bunch` subclass. This allows easy reversion to
            the simple type or simple bypassing of the `Bunch` subclass methods.

    Args:
        contents: stored collection of items.

    """

    contents: Collection[Any]

    """ Required Subclass Methods """

    @abc.abstractmethod
    def add(self, item: Any, *args: Any, **kwargs: Any) -> None:
        """Adds `item` to `contents`.

        Args:
            item: item to add to `contents`.
            args: positional arguments.
            kwargs: keyword arguments.

        """

    @abc.abstractmethod
    def delete(self, item: Any, *args: Any, **kwargs: Any) -> None:
        """Deletes `item` from `contents`.

        Args:
            item: item or key to delete in `contents`.
            args: positional arguments.
            kwargs: keyword arguments.

        Raises:
            KeyError: if `item` is not in `contents`. Subclasses should
                implement this error.

        """

    @abc.abstractmethod
    def subset(
        self,
        include: Collection[Any] | Any | None = None,
        exclude: Collection[Any] | Any | None = None,
        returns: SubsetReturns = settings._SUBSET_RETURN) -> Bunch:
        """Returns a new instance with a subset of `contents`.

        This method applies `include` before `exclude` if both are passed. If
        `include` is None, all existing items will be added to the new subset
        class instance before `exclude` is applied.

        Args:
            include: item(s) to include in the new `Bunch`. Defaults to `None`.
            exclude: item(s) to exclude from the new `Bunch`. Defaults to
                `None`.
            returns: whether to return a new instance of the `Bunch` subclass
                ('class'), a deep copy of the subclass instance ('copy') or the
                simple native Python type ('simple'). Defaults to the global
                setting stored in `settings._SUBSET_RETURN`.

        """

    """ Dunder Methods """

    def __add__(self, other: Any) -> Self:
        """Combines argument with `contents` using the `add` method.

        Args:
            other: item to add to `contents` using the `add` method.

        """
        self.add(item = other)
        return self

    def __iadd__(self, other: Any) -> Self:
        """Combines argument with `contents` using the `add` method.

        Args:
            other: item to add to `contents` using the `add` method.

        """
        self.add(item = other)
        return self

    def __delitem__(self, item: Hashable) -> Self:
        """Deletes `item` from `contents`.

        Args:
            item: item or key to delete in `contents`.

        Raises:
            KeyError: if `item` is not in `contents`.

        """
        self.delete(item = item)
        return self

    def __iter__(self) -> Iterator[Any]:
        """Returns iterator of `contents`.

        Returns:
            Iterator: of `contents`.

        """
        return iter(self.contents)

    def __len__(self) -> int:
        """Returns length of `contents`.

        Returns:
            int: length of `contents`.

        """
        return len(self.contents)
