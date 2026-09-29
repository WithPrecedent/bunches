"""List-like classes

Contents:
    Listing (base.Bunch, MutableSequence): drop-in replacement for a python
        `list` with additional functionality.
    DictList (Listing): iterable with both `dict` and `list` interfaces. Stored
        items must be hashable or have a `name` attribute.

"""

from __future__ import annotations

import copy
import dataclasses
from collections.abc import Hashable, Mapping, MutableSequence
from typing import TYPE_CHECKING, Any

from . import base, settings, utilities

if TYPE_CHECKING:
    from .kinds import GenericList, SubsetReturns


@dataclasses.dataclass
class Listing(base.Bunch, MutableSequence):
    """Basic `list` replacement.

    A `Listing` differs from an ordinary python `list` in ways required by
    inheriting from `Bunch`: `add`, `delete`, and `subset` methods, and allowing
    the "+" operator to join `Listing`s with other `list`-like objects) and in 1
    other way:
        1) It includes a `prepend` method for adding one or more items to the
            beginning of the stored list.

    The `add` method attempts to extend `contents` with the item to be added.
    If it is not a sequence, it appends the item to `contents`.

    Args:
        contents: items to store in a `list`. Defaults to an empty `list`.

    """

    contents: GenericList = dataclasses.field(default_factory=list)

    """ Instance Methods """

    def add(self, item: Any | GenericList) -> None:
        """Extends `contents` with `item` if it is a sequence. Otherwise appends.

        The method will extend all passed sequences, except `str` and `bytes`
        types, which it will append.

        Args:
            item: item(s) to add to `contents`.

        """
        if utilities._is_sequence(item=item):
            self.contents.extend(item)
        else:
            self.contents.append(item)

    def delete(self, item: int | slice) -> None:
        """Deletes item at the index in `contents`.

        Args:
            item: index (or slice) in `contents` to delete.

        Raises:
            IndexError: if `item` is out of range.

        """
        del self.contents[item]

    def insert(self, index: int, item: Any) -> None:
        """Inserts `item` at `index` in `contents`.

        Args:
            index: index to insert `item` at.
            item: object to be inserted.

        """
        self.contents.insert(index, item)

    def prepend(self, item: Any | GenericList) -> None:
        """Prepends `item` to `contents`.

        If `item` is a non-str sequence, `prepend` adds its contents to the
        beginning of the stored list in the order they appear in `item`.

        Args:
            item: item(s) to prepend to `contents`.

        """
        if utilities._is_sequence(item=item):
            self.contents[:0] = list(item)
        else:
            self.insert(0, item)

    def subset(
        self,
        include: Any | GenericList | None = None,
        exclude: Any | GenericList | None = None,
        returns: SubsetReturns | None = None,
    ) -> Any:
        """Returns a new instance with a subset of `contents`.

        This method applies `include` before `exclude` if both are passed. If
        `include` is None, all existing items will be added to the new subset
        class instance before `exclude` is applied.

        Args:
            include: item(s) to include in the new instance. Defaults to `None`.
            exclude: item(s) to exclude in the new instance. Defaults to `None`.
            returns: whether to return a new instance of the `Listing` subclass
                ("class"), a deep copy of the subclass instance ("copy") or the
                simple native Python type ("simple"). Defaults to `None`, which
                uses the global setting stored in `settings._SUBSET_RETURN`.

        Raises:
            ValueError: if `include` and `exclude` are both None.

        Returns:
            Instance with only items from `include` and no items in `exclude`,
                in the form dictated by the `returns` argument.

        """
        if include is None and exclude is None:
            raise ValueError("include or exclude must not be None")
        returns = self._resolve_returns(returns)
        if include is None:
            contents = copy.deepcopy(self.contents)
        else:
            include = list(utilities._iterify(include))
            contents = [i for i in self.contents if i in include]
        if exclude is not None:
            exclude = list(utilities._iterify(exclude))
            contents = [i for i in contents if i not in exclude]
        return utilities._return_subset(
            subset=contents, existing=self, returns=returns
        )

    """ Dunder Methods """

    def __getitem__(self, index: Any) -> Any:
        """Returns value(s) for `index` in `contents`.

        Args:
            index: index (or slice) to search for in `contents`.

        Returns:
            Item(s) stored in `contents` at `index`.

        """
        return self.contents[index]

    def __setitem__(self, index: Any, value: Any) -> None:
        """Sets `index` in `contents` to `value`.

        Args:
            index: index (or slice) to set `value` to in `contents`.
            value: value to be set at `index` in `contents`.

        """
        self.contents[index] = value


@dataclasses.dataclass
class DictList(Listing):
    """Iterable that has both a dict and list interfaces.

    DictList combines the functionality and interfaces of python dicts and lists.
    It allows duplicate keys and list-like iteration while supporting the easier
    access methods of dictionaries. In order to support this hybrid approach to
    iterables, DictList can only store items that are hashable or have a `name`
    attribute or property that contains or returns a hashable value.

    A DictList inherits the differences between a Listing and an ordinary python
    list.

    A DictList differs from a Listing in 4 significant ways:
        1) It only stores hashable items or objects for which a str name can be
            derived (using the global key namer in `settings._KEY_NAMER`).
        2) DictList has an interface of both a dict and a list, but stores a list.
            DictList does this by taking advantage of the `name` attribute or
            hashability of stored items. A `name` or hash acts as a key to
            create the facade of a dict with the items in the stored list
            serving as values. This allows for duplicate keys for storing items,
            simpler iteration than a dict, and support for returning multiple
            matching items. This design comes at the expense of lookup speed. As
            a result, DictList should only be used if a high volume of access
            calls is not anticipated. Ordinarily, the loss of lookup speed
            should have negligible effect on overall performance.
        3) DictLists should not store int types. This ensures that when, for
            example, a `dictlist_instance[3]` is called, the item at that index is
            returned. If int types are stored, that call would create
            uncertainty as to whether an index or item should be returned. By
            design, int types are assumed to be calls to return the item at that
            index.
        4) When using dict access methods, a `DictList` of matches may be
            returned because a DictList allows duplicate pseudo-keys to be used.

    Args:
        contents: items to store that are hashable or have a `name` attribute.
            Defaults to an empty list.
        default_factory: default value to return or default function to call
            when the `get` method is used. Defaults to `None`.

    """

    contents: MutableSequence[Hashable] = dataclasses.field(
        default_factory=list
    )
    default_factory: Any | None = None

    """ Instance Methods """

    def delete(self, item: Any | int | slice) -> None:
        """Deletes item in `contents`.

        If `item` is not an int type, this method looks for a matching `name`
        attribute in the stored instances and deletes all such items. If `item`
        is an int type, only the item at that index is deleted.

        Args:
            item: name or index in `contents` to delete.

        Raises:
            KeyError: if `item` is not an int and no stored item matches it.

        """
        if isinstance(item, int | slice):
            del self.contents[item]
        else:
            namer = settings._KEY_NAMER
            remaining = [c for c in self.contents if namer(c) != item]
            if len(remaining) == len(self.contents):
                raise KeyError(f"{item} is not in {self.__class__.__name__}")
            self.contents[:] = remaining

    def get(self, key: Hashable, default: Any | None = None) -> Any:
        """Returns value in `contents` or default options.

        Args:
            key: name or index for value in `contents`.
            default: default value to return if `key` is not found in
                `contents`.

        Raises:
            KeyError: if `key` is not in the DictList and `default` and the
                `default_factory` attribute are both None.

        Returns:
            Value matching key in `contents`, `default`, or the
                `default_factory` value (called if it is callable).

        """
        try:
            return self[key]
        except (KeyError, IndexError, TypeError) as error:
            if default is not None:
                return default
            if self.default_factory is None:
                raise KeyError(f"{key} is not in the DictList") from error
            if callable(self.default_factory):
                return self.default_factory()
            return self.default_factory

    def items(self) -> tuple[tuple[Hashable, Any], ...]:
        """Emulates python dict `items` method.

        Returns:
            A tuple of (key, value) pairs equivalent to `dict.items()`. A
                DictList cannot actually create an ItemsView because that would
                eliminate any duplicate keys, which are permitted by DictList.

        """
        return tuple(zip(self.keys(), self.values(), strict=True))

    def keys(self) -> tuple[Hashable, ...]:
        """Emulates python dict `keys` method.

        Returns:
            A tuple equivalent to dict.keys(). A DictList cannot actually
                create a KeysView because that would eliminate any duplicate
                keys, which are permitted by DictList.

        """
        namer = settings._KEY_NAMER
        return tuple(namer(c) for c in self.contents)

    def setdefault(self, value: Any) -> None:
        """Sets default value to return when `get` method is used.

        Args:
            value: default value to return.

        """
        self.default_factory = value

    def update(self, items: Mapping[Any, Any]) -> None:
        """Mimics the dict `update` method by extending `contents` with `items`.

        Args:
            items: items to add to the `contents` attribute. The values of
                `items` are added to `contents` and the keys become the `name`
                attributes of those values. As a result, the keys of `items`
                are discarded. To mimic `dict.update`, the passed `items`
                values are added to `contents` by the `extend` method which
                adds the values to the end of `contents`.

        """
        self.extend(list(items.values()))

    def values(self) -> tuple[Any, ...]:
        """Emulates python dict `values` method.

        Returns:
            A tuple equivalent to dict.values(). A DictList cannot actually
                create a ValuesView because that would eliminate any duplicate
                keys, which are permitted by DictList.

        """
        return tuple(self.contents)

    """ Dunder Methods """

    def __getitem__(self, key: Hashable | int | slice) -> Any:
        """Returns value(s) for `key` in `contents`.

        If `key` is not an int type, this method looks for a matching `name`
        attribute in the stored instances.

        If `key` is an int (or a slice), this method returns the stored item(s)
        at the corresponding index.

        If only one match is found, a single item is returned. If more are
        found, a `DictList` or `DictList` subclass with the matching stored
        items is returned.

        Args:
            key: name of an item or index to search for in `contents`.

        Raises:
            KeyError: if `key` is not an int or slice and no item matches it.
            IndexError: if `key` is an int outside of the range of `contents`.

        Returns:
            Value(s) stored in `contents` that correspond to `key`. If there is
                more than one match, the return is a DictList or DictList
                subclass with the matching stored items.

        """
        if isinstance(key, int | slice):
            return self.contents[key]
        namer = settings._KEY_NAMER
        matches = [c for c in self.contents if namer(c) == key]
        if not matches:
            raise KeyError(f"{key} is not in {self.__class__.__name__}")
        if len(matches) == 1:
            return matches[0]
        return self.__class__(
            contents=matches, default_factory=self.default_factory
        )

    def __setitem__(self, key: Any | int | slice, value: Any) -> None:
        """Sets `key` in `contents` to `value`.

        Args:
            key: if key isn't an int or slice, it is ignored (since the `name`
                attribute of the value will be acting as the key). In such a
                case, the `value` is added to the end of `contents`. If key is
                an int, `value` is assigned at the that index number in
                `contents`.
            value: value to be paired with `key` in `contents`.

        """
        if isinstance(key, int | slice):
            self.contents[key] = value
        else:
            self.add(value)
