"""Base class for extensible, flexible, lightweight collection types.

Contents:
    Bunch (Collection, abc.ABC): base class for collections in `bunches`. It
        requires subclasses to have `add`, `delete`, and `subset` methods.

"""

from __future__ import annotations

import abc
import copy
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
            designate the preferred method of adding to the collection's stored
            data without replacing other access methods.
        2) It must include a `delete` method which provides the default
            mechanism for deleting items in the collection. `delete` is called
            by the `__delitem__` dunder method to delete stored items.
        3) A subclass must include a `subset` method with optional `include` and
            `exclude` parameters for returning a subset of the Bunch subclass.
        4) It supports the '+' and '+=' operators being used to join a Bunch
            subclass instance with an item of the same python type (mapping,
            sequence, etc.). Both operators call the Bunch subclass `add`
            method to implement how the added item(s) is/are added. '+' leaves
            the original instance unchanged and returns a modified deep copy,
            while '+=' modifies the instance in place.
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
            *args: positional arguments.
            **kwargs: keyword arguments.

        """

    @abc.abstractmethod
    def delete(self, item: Any, *args: Any, **kwargs: Any) -> None:
        """Deletes `item` from `contents`.

        Args:
            item: item or key to delete in `contents`.
            *args: positional arguments.
            **kwargs: keyword arguments.

        Raises:
            KeyError: if `item` is not in `contents`. Subclasses should
                implement this error.

        """

    @abc.abstractmethod
    def subset(
        self,
        include: Collection[Any] | Any | None = None,
        exclude: Collection[Any] | Any | None = None,
        returns: SubsetReturns | None = None,
    ) -> Any:
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
                simple native Python type ('simple'). Defaults to `None`, which
                uses the global setting stored in `settings._SUBSET_RETURN`.

        Returns:
            A subset of the stored data in the form dictated by `returns`.

        """

    """ Dunder Methods """

    def __add__(self, other: Any) -> Self:
        """Returns a deep copy with `other` combined using the `add` method.

        Args:
            other: item to add to the copy's `contents` using the `add` method.

        Returns:
            A new instance. The original instance is not modified.

        """
        new_instance = copy.deepcopy(self)
        new_instance.add(item=other)
        return new_instance

    def __iadd__(self, other: Any) -> Self:
        """Combines argument with `contents` using the `add` method.

        Args:
            other: item to add to `contents` using the `add` method.

        Returns:
            The instance, modified in place.

        """
        self.add(item=other)
        return self

    def __delitem__(self, item: Hashable) -> None:
        """Deletes `item` from `contents`.

        Args:
            item: item or key to delete in `contents`.

        Raises:
            KeyError: if `item` is not in `contents`.

        """
        self.delete(item=item)

    def __iter__(self) -> Iterator[Any]:
        """Returns iterator of `contents`.

        Returns:
            Iterator of `contents`.

        """
        return iter(self.contents)

    def __len__(self) -> int:
        """Returns length of `contents`.

        Returns:
            Length of `contents`.

        """
        return len(self.contents)

    """ Private Methods """

    def _resolve_returns(self, returns: SubsetReturns | None) -> SubsetReturns:
        """Returns `returns` or the global default if it is `None`.

        Args:
            returns: `returns` argument passed to a `subset` method.

        Returns:
            'returns' or the value of `settings._SUBSET_RETURN`.

        """
        return settings._SUBSET_RETURN if returns is None else returns
