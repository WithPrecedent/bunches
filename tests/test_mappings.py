"""Tests for `bunches.mappings`."""

from __future__ import annotations

import pytest

from bunches import Catalog, ChainDict, Dictionary, Repository, settings

from .conftest import Another, Something, Unnamed


class TestDictionary:
    """Tests for `Dictionary`."""

    def test_init(self) -> None:
        """Tests defaults."""
        dictionary = Dictionary()
        assert dictionary.contents == {}
        assert dictionary.default_factory is None
        assert len(dictionary) == 0

    def test_fromkeys(self) -> None:
        """Tests `fromkeys`."""
        dictionary = Dictionary.fromkeys(['a', 'b'], 'tree')
        assert isinstance(dictionary, Dictionary)
        assert dictionary.contents == {'a': 'tree', 'b': 'tree'}
        dictionary = Dictionary.fromkeys(['a'], 1, default_factory = 5)
        assert dictionary.default_factory == 5

    def test_add(self) -> None:
        """Tests `add`."""
        dictionary = Dictionary({'a': 1})
        dictionary.add({'b': 2})
        dictionary.add({'c': 3}, d = 4)
        assert dictionary.contents == {'a': 1, 'b': 2, 'c': 3, 'd': 4}

    def test_delete(self) -> None:
        """Tests `delete` and `__delitem__`."""
        dictionary = Dictionary({'a': 1, 'b': 2, 'c': 3})
        dictionary.delete('a')
        del dictionary['b']
        assert dictionary.contents == {'c': 3}
        with pytest.raises(KeyError):
            dictionary.delete('missing')
        with pytest.raises(KeyError):
            del dictionary['missing']

    def test_get(self) -> None:
        """Tests `get` with and without defaults."""
        dictionary = Dictionary({'a': 1})
        assert dictionary.get('a') == 1
        assert dictionary.get('b', 3) == 3
        with pytest.raises(KeyError):
            dictionary.get('b')
        with pytest.raises(KeyError):
            dictionary.get(['unhashable'])
        dictionary.default_factory = 'Nada'
        assert dictionary.get('b') == 'Nada'
        assert dictionary.get('b', 3) == 3
        dictionary.default_factory = list
        assert dictionary.get('b') == []
        assert dictionary.get('b') is not dictionary.get('b')
        assert dictionary.get('a') == 1

    def test_setdefault(self) -> None:
        """Tests `setdefault`."""
        dictionary = Dictionary()
        dictionary.setdefault('No')
        assert dictionary.default_factory == 'No'
        assert dictionary.get('anything') == 'No'

    def test_keys_values_items(self) -> None:
        """Tests that `keys`, `values` and `items` return tuples."""
        dictionary = Dictionary({'a': 1, 'b': 2})
        assert dictionary.keys() == ('a', 'b')
        assert dictionary.values() == (1, 2)
        assert dictionary.items() == (('a', 1), ('b', 2))
        assert dict(dictionary) == {'a': 1, 'b': 2}

    def test_getitem_setitem(self) -> None:
        """Tests `__getitem__` and `__setitem__`."""
        dictionary = Dictionary({'a': 1})
        dictionary['b'] = 2
        assert dictionary['a'] == 1
        assert dictionary['b'] == 2
        assert 'b' in dictionary
        assert 'c' not in dictionary
        with pytest.raises(KeyError):
            dictionary['c']

    def test_mutable_mapping_methods(self) -> None:
        """Tests methods inherited from `MutableMapping`."""
        dictionary = Dictionary({'a': 1, 'b': 2})
        assert list(dictionary) == ['a', 'b']
        assert dictionary.pop('a') == 1
        dictionary.update({'z': 26})
        assert dictionary.contents == {'b': 2, 'z': 26}
        dictionary.clear()
        assert dictionary.contents == {}

    def test_subset(self) -> None:
        """Tests `subset` with `include` and `exclude`."""
        dictionary = Dictionary({'a': 1, 'b': 2, 'c': 3}, default_factory = 0)
        subset = dictionary.subset(include = ['a', 'b'])
        assert isinstance(subset, Dictionary)
        assert subset.contents == {'a': 1, 'b': 2}
        assert dictionary.subset(include = 'c').contents == {'c': 3}
        assert dictionary.subset(exclude = 'a').contents == {'b': 2, 'c': 3}
        assert dictionary.subset(
            include = ['a', 'b'], exclude = ['b']).contents == {'a': 1}
        assert dictionary.contents == {'a': 1, 'b': 2, 'c': 3}
        with pytest.raises(ValueError, match = 'must not be None'):
            dictionary.subset()
        with pytest.raises(KeyError):
            dictionary.subset(include = 'missing')

    def test_subset_returns(self) -> None:
        """Tests the `returns` argument of `subset`."""
        dictionary = Dictionary({'a': 1, 'b': 2}, default_factory = 0)
        assert dictionary.subset(include = 'a', returns = 'simple') == {'a': 1}
        copied = dictionary.subset(include = 'a', returns = 'copy')
        assert isinstance(copied, Dictionary)
        assert copied.default_factory == 0
        assert copied.contents == {'a': 1}
        assert dictionary.subset(include = 'a').default_factory is None
        with pytest.raises(ValueError, match = 'returns argument'):
            dictionary.subset(include = 'a', returns = 'other')  # type: ignore[arg-type]
        settings.set_subset_return('simple')
        assert dictionary.subset(include = 'a') == {'a': 1}

    def test_subset_exclude_is_deep_copy(self) -> None:
        """Tests that excluding only does not share mutable values."""
        dictionary = Dictionary({'a': [1], 'b': [2]})
        subset = dictionary.subset(exclude = 'b')
        subset['a'].append(5)
        assert dictionary['a'] == [1]

    def test_add_operators(self) -> None:
        """Tests `+` and `+=`."""
        dictionary = Dictionary({'a': 1})
        combined = dictionary + {'b': 2}
        assert combined.contents == {'a': 1, 'b': 2}
        assert dictionary.contents == {'a': 1}
        assert (dictionary + Dictionary({'c': 3})).contents == {'a': 1, 'c': 3}
        dictionary += {'b': 2}
        assert dictionary.contents == {'a': 1, 'b': 2}

    def test_equality_and_repr(self) -> None:
        """Tests equality and `repr`."""
        assert Dictionary({'a': 1}) == Dictionary({'a': 1})
        assert Dictionary({'a': 1}) != Dictionary({'a': 2})
        assert 'contents' in repr(Dictionary({'a': 1}))


class TestCatalog:
    """Tests for `Catalog`."""

    @pytest.fixture
    def catalog(self) -> Catalog:
        """Returns a `Catalog` with three items."""
        return Catalog(contents = {
            'tester': Something,
            'another': Another,
            'a_third': Unnamed()})

    def test_init(self) -> None:
        """Tests defaults."""
        catalog = Catalog()
        assert catalog.contents == {}
        assert catalog.default == 'all'
        assert catalog.always_return_list is False

    def test_direct_access(self, catalog: Catalog) -> None:
        """Tests direct key access and membership."""
        assert catalog['tester'] is Something
        assert 'tester' in catalog
        assert 'another' in catalog
        assert 'a_third' in catalog
        assert len(catalog) == 3
        with pytest.raises(KeyError, match = 'missing'):
            catalog['missing']

    def test_all(self, catalog: Catalog) -> None:
        """Tests the `all` wildcard."""
        values = catalog['all']
        assert isinstance(values, list)
        assert len(values) == 3
        assert catalog['All'] == values
        assert catalog[['all']] == values

    def test_default(self, catalog: Catalog) -> None:
        """Tests the `default` wildcard."""
        assert catalog['default'] == catalog['all']
        catalog.default = 'tester'
        assert catalog['default'] is Something
        catalog.default = ['tester', 'another']
        assert catalog['default'] == [Something, Another]
        assert catalog['Defaults'] == [Something, Another]

    def test_none(self, catalog: Catalog) -> None:
        """Tests the `none` wildcard."""
        assert catalog['none'] is None
        assert catalog['None'] is None
        catalog.always_return_list = True
        assert catalog['none'] == []
        catalog.always_return_list = False
        catalog.default_factory = 'nothing'
        assert catalog['none'] == 'nothing'
        catalog.default_factory = list
        assert catalog['none'] == []

    def test_list_of_keys(self, catalog: Catalog) -> None:
        """Tests accessing a list of keys."""
        assert catalog[['tester', 'another']] == [Something, Another]
        assert catalog[('tester',)] == [Something]
        assert catalog[['tester', 'missing']] == [Something]

    def test_always_return_list(self, catalog: Catalog) -> None:
        """Tests `always_return_list`."""
        catalog.always_return_list = True
        assert catalog['tester'] == [Something]
        with pytest.raises(KeyError):
            catalog['missing']

    def test_setitem(self, catalog: Catalog) -> None:
        """Tests `__setitem__` with a key and with a list of keys."""
        catalog['fourth'] = 4
        assert catalog['fourth'] == 4
        catalog[['fifth', 'sixth']] = [5, 6]
        assert catalog['fifth'] == 5
        assert catalog['sixth'] == 6
        with pytest.raises(ValueError, match = 'shorter|longer'):
            catalog[['a', 'b']] = [1]

    def test_add_and_get(self, catalog: Catalog) -> None:
        """Tests `add` and `get`."""
        catalog.add({'new': 1})
        assert catalog['new'] == 1
        assert catalog.get('new') == 1
        assert catalog.get('missing', 'x') == 'x'
        catalog.default_factory = 'nothing'
        assert catalog.get('missing') == 'nothing'

    def test_delete(self, catalog: Catalog) -> None:
        """Tests `delete` with one and several keys."""
        catalog.delete('a_third')
        assert 'a_third' not in catalog
        del catalog[['tester', 'another']]
        assert 'tester' not in catalog
        assert len(catalog) == 0

    def test_delete_missing(self, catalog: Catalog) -> None:
        """Tests that `delete` raises and does not change anything."""
        with pytest.raises(KeyError, match = 'not found'):
            catalog.delete(['tester', 'missing'])
        assert len(catalog) == 3
        with pytest.raises(KeyError):
            catalog.delete('missing')

    def test_delete_preserves_container(self) -> None:
        """Tests that `delete` modifies `contents` in place."""
        contents = {'a': 1, 'b': 2}
        catalog = Catalog(contents = contents)
        catalog.delete('a')
        assert catalog.contents is contents
        assert contents == {'b': 2}

    def test_subset(self, catalog: Catalog) -> None:
        """Tests `subset`."""
        subset = catalog.subset(include = ['tester', 'another'])
        assert isinstance(subset, Catalog)
        assert subset.contents == {'tester': Something, 'another': Another}
        simple = catalog.subset(exclude = 'tester', returns = 'simple')
        assert isinstance(simple, dict)
        assert list(simple) == ['another', 'a_third']


class TestChainDict:
    """Tests for `ChainDict`."""

    @pytest.fixture
    def chain(self) -> ChainDict:
        """Returns a `ChainDict` with two mappings that share a key."""
        return ChainDict(contents = [
            Dictionary({'a': 1, 'b': 2}),
            Dictionary({'a': 10, 'c': 30})])

    def test_init(self) -> None:
        """Tests defaults."""
        chain = ChainDict()
        assert chain.contents == []
        assert chain.return_first is True
        assert len(chain) == 0
        assert list(chain) == []

    def test_maps(self, chain: ChainDict) -> None:
        """Tests the `maps` property."""
        assert chain.maps is chain.contents
        chain.maps = [Dictionary({'z': 1})]
        assert chain.contents == [Dictionary({'z': 1})]
        del chain.maps
        assert chain.contents == []

    def test_fromkeys(self) -> None:
        """Tests `fromkeys`."""
        chain = ChainDict.fromkeys(['a', 'b'], 1)
        assert isinstance(chain, ChainDict)
        assert chain.keys() == ('a', 'b')
        assert chain['a'] == 1
        assert len(chain.contents) == 1

    def test_getitem_return_first(self, chain: ChainDict) -> None:
        """Tests `__getitem__` when returning only the first match."""
        assert chain['a'] == 1
        assert chain['b'] == 2
        assert chain['c'] == 30
        with pytest.raises(KeyError, match = 'missing'):
            chain['missing']

    def test_getitem_all_matches(self, chain: ChainDict) -> None:
        """Tests `__getitem__` when returning all matches."""
        chain.return_first = False
        assert chain['a'] == [1, 10]
        assert chain['b'] == 2
        assert chain['c'] == 30
        with pytest.raises(KeyError):
            chain['missing']

    def test_setitem(self, chain: ChainDict) -> None:
        """Tests `__setitem__`, including on an empty `ChainDict`."""
        chain['z'] = 26
        assert chain.contents[0]['z'] == 26
        assert 'z' not in chain.contents[1]
        empty = ChainDict()
        empty['a'] = 1
        assert empty.contents == [Dictionary({'a': 1})]
        assert empty['a'] == 1

    def test_keys_values_items(self, chain: ChainDict) -> None:
        """Tests `keys`, `values` and `items`."""
        assert chain.keys() == ('a', 'b', 'a', 'c')
        assert chain.values() == (1, 2, 10, 30)
        assert chain.items() == (('a', 1), ('b', 2), ('a', 10), ('c', 30))

    def test_mapping_interface(self, chain: ChainDict) -> None:
        """Tests iteration and length use keys, as in any mapping."""
        assert list(chain) == ['a', 'b', 'a', 'c']
        assert len(chain) == 4
        assert 'c' in chain
        assert 'z' not in chain
        assert dict(chain) == {'a': 1, 'b': 2, 'c': 30}

    def test_add(self, chain: ChainDict) -> None:
        """Tests `add` with `Dictionary` instances and plain mappings."""
        chain.add(Dictionary({'x': 1}))
        chain.add({'y': 2})
        chain.add({'z': 3}, w = 4)
        chain.add(Dictionary({'v': 5}), u = 6)
        assert len(chain.contents) == 6
        assert all(isinstance(d, Dictionary) for d in chain.contents)
        assert chain['y'] == 2
        assert chain.contents[4].contents == {'z': 3, 'w': 4}
        assert chain.contents[5].contents == {'v': 5, 'u': 6}

    def test_delete(self, chain: ChainDict) -> None:
        """Tests `delete` removes a key from every stored mapping."""
        chain.delete('a')
        assert chain.keys() == ('b', 'c')
        del chain['b']
        assert chain.keys() == ('c',)
        with pytest.raises(KeyError, match = 'missing'):
            chain.delete('missing')

    def test_new_child_and_parents(self, chain: ChainDict) -> None:
        """Tests `new_child` and `parents`."""
        chain.default_factory = 'nothing'
        chain.return_first = False
        chain.new_child(Dictionary({'a': 0}))
        assert chain['a'] == [0, 1, 10]
        parents = chain.parents()
        assert isinstance(parents, ChainDict)
        assert len(parents.contents) == 2
        assert parents.default_factory == 'nothing'
        assert parents.return_first is False
        assert len(chain.contents) == 3

    def test_subset(self, chain: ChainDict) -> None:
        """Tests `subset`, including keys missing from some mappings."""
        subset = chain.subset(include = ['a', 'c'])
        assert isinstance(subset, ChainDict)
        assert subset.keys() == ('a', 'a', 'c')
        assert subset.values() == (1, 10, 30)
        subset = chain.subset(exclude = 'a')
        assert subset.keys() == ('b', 'c')
        subset = chain.subset(include = 'b')
        assert subset.keys() == ('b',)
        assert len(subset.contents) == 2
        assert chain.keys() == ('a', 'b', 'a', 'c')
        with pytest.raises(ValueError, match = 'must not be None'):
            chain.subset()

    def test_subset_returns(self, chain: ChainDict) -> None:
        """Tests the `returns` argument of `subset`."""
        chain.default_factory = 'nothing'
        copied = chain.subset(include = 'a', returns = 'copy')
        assert copied.default_factory == 'nothing'
        simple = chain.subset(include = 'a', returns = 'simple')
        assert isinstance(simple, list)
        assert simple[0] == Dictionary({'a': 1})

    def test_mutable_mapping_methods(self, chain: ChainDict) -> None:
        """Tests methods inherited from `MutableMapping`."""
        chain.update({'q': 5})
        assert chain.contents[0]['q'] == 5
        assert chain.pop('q') == 5
        assert 'q' not in chain


class TestRepository:
    """Tests for `Repository`."""

    def test_init(self) -> None:
        """Tests defaults."""
        repository = Repository()
        assert repository.contents == {}
        assert repository.overwrite is False

    def test_add_infers_names(self) -> None:
        """Tests that `add` infers keys."""
        repository = Repository()
        repository.add(Another())
        repository.add(Unnamed())
        repository.add('a_string')
        repository.add(Something)
        assert repository.keys() == (
            'another', 'unnamed', 'a_string', 'something')

    def test_add_explicit_key(self) -> None:
        """Tests `add` with a key."""
        repository = Repository()
        repository.add(Something, 'random_name')
        repository.add(Another(), key = 'other')
        assert repository['random_name'] is Something
        assert 'other' in repository
        repository.add(Another(), key = 'other')
        assert repository.keys() == ('random_name', 'other', 'other2')

    def test_add_unique_keys(self) -> None:
        """Tests that keys are made unique when `overwrite` is `False`."""
        repository = Repository()
        for _ in range(3):
            repository.add(Another())
        assert repository.keys() == ('another', 'another2', 'another3')

    def test_add_overwrite(self) -> None:
        """Tests that items are overwritten when `overwrite` is `True`."""
        repository = Repository(overwrite = True)
        first = Another('same')
        second = Another('same')
        repository.add(first)
        repository.add(second)
        assert repository.keys() == ('same',)
        assert repository['same'] is second

    def test_add_kwargs(self) -> None:
        """Tests that extra keyword arguments are stored."""
        repository = Repository()
        repository.add(Another(), extra = 1)
        assert repository['extra'] == 1

    def test_get_name_override(self) -> None:
        """Tests that a subclass can change how names are inferred."""

        class Numbered(Repository):
            def _get_name(self, item: object) -> str:
                return f'item_{len(self)}'

        repository = Numbered()
        repository.add('a')
        repository.add('b')
        assert repository.keys() == ('item_0', 'item_1')

    def test_get_name(self) -> None:
        """Tests `_get_name`, which uses the global key namer."""
        repository = Repository()
        assert repository._get_name(Something()) == 'something'
        settings.set_key_namer(lambda item: 'same')
        assert repository._get_name(Something()) == 'same'

    def test_delete(self) -> None:
        """Tests `delete`."""
        repository = Repository()
        repository.add(Another())
        repository.add(Something, 'random_name')
        repository.delete('random_name')
        assert 'random_name' not in repository
        assert 'another' in repository
        with pytest.raises(KeyError):
            repository.delete('random_name')

    def test_subset(self) -> None:
        """Tests `subset` keeps `Repository` behavior."""
        repository = Repository(overwrite = True)
        repository.add(Another())
        repository.add(Something())
        subset = repository.subset(include = 'another', returns = 'copy')
        assert isinstance(subset, Repository)
        assert subset.overwrite is True
        assert subset.keys() == ('another',)
