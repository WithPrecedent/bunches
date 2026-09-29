"""Tests for `bunches.sequences`."""

from __future__ import annotations

import pytest

from bunches import DictList, Listing, settings

from .conftest import Another, Something


class TestListing:
    """Tests for `Listing`."""

    def test_init(self) -> None:
        """Tests defaults."""
        listing = Listing()
        assert listing.contents == []
        assert len(listing) == 0

    def test_add(self) -> None:
        """Tests `add` extends with sequences and appends everything else."""
        listing = Listing(['a'])
        listing.add('bc')
        listing.add(['d', 'e'])
        listing.add(('f', 'g'))
        listing.add(b'h')
        listing.add(7)
        listing.add({'set'})
        assert listing.contents == [
            'a', 'bc', 'd', 'e', 'f', 'g', b'h', 7, {'set'}]

    def test_delete(self) -> None:
        """Tests `delete` and `__delitem__`."""
        listing = Listing(['a', 'b', 'c', 'd'])
        listing.delete(0)
        del listing[0]
        assert listing.contents == ['c', 'd']
        listing.delete(slice(0, 2))
        assert listing.contents == []
        with pytest.raises(IndexError):
            listing.delete(0)

    def test_insert_and_prepend(self) -> None:
        """Tests `insert` and `prepend`."""
        listing = Listing(['c'])
        listing.insert(0, 'b')
        listing.prepend('a')
        assert listing.contents == ['a', 'b', 'c']
        listing.prepend(['x', 'y'])
        assert listing.contents == ['x', 'y', 'a', 'b', 'c']
        listing.prepend([['nested']])
        assert listing.contents[0] == ['nested']
        listing.prepend([])
        assert len(listing) == 6

    def test_getitem_setitem(self) -> None:
        """Tests `__getitem__` and `__setitem__`."""
        listing = Listing(['a', 'b', 'c'])
        assert listing[1] == 'b'
        assert listing[-1] == 'c'
        assert listing[0:2] == ['a', 'b']
        listing[1] = 'z'
        assert listing.contents == ['a', 'z', 'c']
        listing[0:2] = ['x']
        assert listing.contents == ['x', 'c']
        with pytest.raises(IndexError):
            listing[5]

    def test_mutable_sequence_methods(self) -> None:
        """Tests methods inherited from `MutableSequence`."""
        listing = Listing(['a', 'b', 'c'])
        listing.append('d')
        listing.extend(['e', 'f'])
        assert listing.contents == ['a', 'b', 'c', 'd', 'e', 'f']
        listing.remove('b')
        assert listing.pop() == 'f'
        assert listing.index('c') == 1
        assert listing.count('a') == 1
        listing.reverse()
        assert listing.contents == ['e', 'd', 'c', 'a']
        assert 'a' in listing
        assert list(reversed(listing)) == ['a', 'c', 'd', 'e']
        listing.clear()
        assert listing.contents == []

    def test_subset(self) -> None:
        """Tests `subset`."""
        listing = Listing(['a', 'b', 'c', 'd'])
        subset = listing.subset(include = ['a', 'b', 'c'], exclude = 'b')
        assert isinstance(subset, Listing)
        assert subset.contents == ['a', 'c']
        assert listing.subset(include = 'a').contents == ['a']
        assert listing.subset(exclude = ['a', 'b']).contents == ['c', 'd']
        assert listing.contents == ['a', 'b', 'c', 'd']
        with pytest.raises(ValueError, match = 'must not be None'):
            listing.subset()

    def test_subset_preserves_order_of_contents(self) -> None:
        """Tests `subset` follows the order of `contents`, not `include`."""
        listing = Listing(['a', 'b', 'c'])
        assert listing.subset(include = ['c', 'a']).contents == ['a', 'c']

    def test_subset_returns(self) -> None:
        """Tests the `returns` argument of `subset`."""
        listing = Listing(['a', 'b'])
        assert listing.subset(include = 'a', returns = 'simple') == ['a']
        assert isinstance(listing.subset(include = 'a', returns = 'copy'), Listing)
        with pytest.raises(ValueError, match = 'returns argument'):
            listing.subset(include = 'a', returns = 'other')  # type: ignore[arg-type]
        settings.set_subset_return('simple')
        assert listing.subset(include = 'a') == ['a']

    def test_add_operators(self) -> None:
        """Tests `+` and `+=`."""
        listing = Listing(['a'])
        combined = listing + ['b', 'c']
        assert combined.contents == ['a', 'b', 'c']
        assert listing.contents == ['a']
        assert (listing + 'z').contents == ['a', 'z']
        listing += ['b']
        listing += 'c'
        assert listing.contents == ['a', 'b', 'c']

    def test_equality(self) -> None:
        """Tests equality."""
        assert Listing([1, 2]) == Listing([1, 2])
        assert Listing([1, 2]) != Listing([2, 1])


class TestDictList:
    """Tests for `DictList`."""

    @pytest.fixture
    def dictlist(self) -> DictList:
        """Returns a `DictList` of strings."""
        return DictList(['a', 'b', 'c'])

    def test_init(self) -> None:
        """Tests defaults."""
        dictlist = DictList()
        assert dictlist.contents == []
        assert dictlist.default_factory is None

    def test_list_interface(self, dictlist: DictList) -> None:
        """Tests list behavior inherited from `Listing`."""
        dictlist.add('d')
        assert dictlist[3] == 'd'
        dictlist.insert(2, 'zebra')
        assert dictlist[2] == 'zebra'
        dictlist.append('e')
        dictlist.extend(['f', 'g'])
        assert dictlist.contents == [
            'a', 'b', 'zebra', 'c', 'd', 'e', 'f', 'g']
        dictlist.prepend('first')
        assert dictlist[0] == 'first'
        assert dictlist[1:3] == ['a', 'b']
        dictlist[0] = 'start'
        dictlist[1:3] = ['x', 'y']
        assert dictlist.contents[:4] == ['start', 'x', 'y', 'zebra']

    def test_getitem_by_name(self) -> None:
        """Tests `__getitem__` with names, attributes and multiple matches."""
        something = Something()
        dictlist = DictList([something, Another(), 'plain', Something('x')])
        assert dictlist['something'] is something
        assert dictlist['another'] == Another()
        assert dictlist['plain'] == 'plain'
        assert dictlist['x'] == Something('x')
        with pytest.raises(KeyError, match = 'missing'):
            dictlist['missing']
        with pytest.raises(IndexError):
            dictlist[10]

    def test_getitem_multiple_matches(self) -> None:
        """Tests that duplicate names return a `DictList` of matches."""
        dictlist = DictList(['a', 'b', 'a'], default_factory = 'nope')
        matches = dictlist['a']
        assert isinstance(matches, DictList)
        assert matches.contents == ['a', 'a']
        assert matches.default_factory == 'nope'
        assert dictlist['b'] == 'b'

    def test_setitem(self, dictlist: DictList) -> None:
        """Tests `__setitem__` with an index and with a name."""
        dictlist[0] = 'z'
        assert dictlist.contents == ['z', 'b', 'c']
        dictlist['ignored'] = 'd'
        assert dictlist.contents == ['z', 'b', 'c', 'd']
        dictlist['ignored'] = ['e', 'f']
        assert dictlist.contents == ['z', 'b', 'c', 'd', 'e', 'f']

    def test_get(self, dictlist: DictList) -> None:
        """Tests `get` with and without defaults."""
        assert dictlist.get('a') == 'a'
        assert dictlist.get(1) == 'b'
        assert dictlist.get('tree', 'No') == 'No'
        with pytest.raises(KeyError, match = 'tree'):
            dictlist.get('tree')
        with pytest.raises(KeyError):
            dictlist.get(10)
        dictlist.setdefault(value = 'No')
        assert dictlist.default_factory == 'No'
        assert dictlist.get('tree') == 'No'
        assert dictlist.get(10) == 'No'
        assert dictlist.get('tree', 'Other') == 'Other'
        dictlist.default_factory = list
        assert dictlist.get('tree') == []

    def test_keys_values_items(self) -> None:
        """Tests `keys`, `values` and `items`."""
        something = Something()
        dictlist = DictList(['a', something, 'a'])
        assert dictlist.keys() == ('a', 'something', 'a')
        assert dictlist.values() == ('a', something, 'a')
        assert dictlist.items() == (
            ('a', 'a'), ('something', something), ('a', 'a'))

    def test_update(self, dictlist: DictList) -> None:
        """Tests `update`, which discards the keys."""
        dictlist.update({'ignored': 'd', 'also_ignored': 'e'})
        assert dictlist.contents == ['a', 'b', 'c', 'd', 'e']

    def test_delete(self) -> None:
        """Tests `delete` by index, by slice, and by name."""
        dictlist = DictList(['a', 'b', 'a', 'c', 'd', 'e'])
        dictlist.delete(0)
        assert dictlist.contents == ['b', 'a', 'c', 'd', 'e']
        dictlist.delete('a')
        assert dictlist.contents == ['b', 'c', 'd', 'e']
        del dictlist['b']
        assert dictlist.contents == ['c', 'd', 'e']
        dictlist.delete(slice(0, 2))
        assert dictlist.contents == ['e']
        with pytest.raises(KeyError, match = 'missing'):
            dictlist.delete('missing')
        with pytest.raises(IndexError):
            dictlist.delete(5)

    def test_delete_preserves_container(self) -> None:
        """Tests that deleting by name modifies `contents` in place."""
        contents = ['a', 'b', 'a']
        dictlist = DictList(contents)
        dictlist.delete('a')
        assert dictlist.contents is contents
        assert contents == ['b']

    def test_remove(self) -> None:
        """Tests `remove` inherited from `MutableSequence`."""
        dictlist = DictList(['a', 'b', 'c'])
        dictlist.remove('b')
        assert dictlist.contents == ['a', 'c']

    def test_subset(self) -> None:
        """Tests `subset`."""
        dictlist = DictList(['a', 'b', 'c', 'd', 'zebra'])
        subset = dictlist.subset(
            include = ['a', 'b', 'c', 'zebra'], exclude = 'c')
        assert isinstance(subset, DictList)
        assert subset.contents == ['a', 'b', 'zebra']
        assert subset['zebra'] == 'zebra'
        copied = dictlist.subset(exclude = 'a', returns = 'copy')
        assert copied.contents == ['b', 'c', 'd', 'zebra']
        assert dictlist.contents == ['a', 'b', 'c', 'd', 'zebra']

    def test_hybrid_use(self) -> None:
        """Tests a mix of dict and list access on the same instance."""
        dictlist = DictList(['a', 'b', 'c'])
        dictlist.setdefault(value = 'No')
        assert dictlist.get('tree') == 'No'
        assert dictlist[1] == 'b'
        dictlist.append('b')
        assert dictlist.values() == ('a', 'b', 'c', 'b')
        assert dictlist.keys() == ('a', 'b', 'c', 'b')
        dictlist.clear()
        item = Something()
        dictlist.add(item)
        assert dictlist.keys() == ('something',)
        assert dictlist.values() == (item,)
