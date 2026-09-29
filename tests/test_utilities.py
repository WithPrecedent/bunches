"""Tests for `bunches.utilities`."""

from __future__ import annotations

import dataclasses

import pytest

from bunches import Dictionary, Listing, utilities

from .conftest import Something, Unnamed


def test_capitalify() -> None:
    """Tests `_capitalify`."""
    assert utilities._capitalify('snake_case_name') == 'SnakeCaseName'
    assert utilities._capitalify('word') == 'Word'
    assert utilities._capitalify('') == ''


def test_snakify() -> None:
    """Tests `_snakify`."""
    assert utilities._snakify('SnakeCaseName') == 'snake_case_name'
    assert utilities._snakify('Word') == 'word'
    assert utilities._snakify('HTTPServer') == 'http_server'
    assert utilities._snakify('already_snake') == 'already_snake'


def test_is_sequence() -> None:
    """Tests `_is_sequence`."""
    assert utilities._is_sequence([1, 2])
    assert utilities._is_sequence((1, 2))
    assert utilities._is_sequence(list)
    assert not utilities._is_sequence('abc')
    assert not utilities._is_sequence(str)
    assert not utilities._is_sequence(b'abc')
    assert not utilities._is_sequence({'a': 1})
    assert not utilities._is_sequence({1, 2})
    assert not utilities._is_sequence(5)


def test_iterify() -> None:
    """Tests `_iterify`."""
    assert list(utilities._iterify(None)) == []
    assert list(utilities._iterify('abc')) == ['abc']
    assert list(utilities._iterify(b'abc')) == [b'abc']
    assert list(utilities._iterify([1, 2])) == [1, 2]
    assert list(utilities._iterify((1, 2))) == [1, 2]
    assert list(utilities._iterify(5)) == [5]
    assert list(utilities._iterify({'a': 1})) == ['a']


def test_namify() -> None:
    """Tests `_namify`."""

    @dataclasses.dataclass
    class BadName:
        name: int = 3

    assert utilities._namify('name') == 'name'
    assert utilities._namify(Something()) == 'something'
    assert utilities._namify(Something('other')) == 'other'
    assert utilities._namify(Unnamed()) == 'unnamed'
    assert utilities._namify(Unnamed) == 'unnamed'
    assert utilities._namify(Something) == 'something'
    assert utilities._namify(test_namify) == 'test_namify'
    assert utilities._namify(5) == 'int'
    assert utilities._namify(BadName()) == 'bad_name'


def test_namify_default() -> None:
    """Tests the `default` argument of `_namify`."""

    class Meta(type):
        """Metaclass whose classes have no usable name."""

        @property
        def __name__(cls) -> str:  # type: ignore[override]
            return ''

    class Nameless(metaclass = Meta):
        """Class without a usable name."""

    assert utilities._namify(Nameless(), default = 'fallback') == 'fallback'
    assert utilities._namify(Nameless()) is None


def test_return_subset() -> None:
    """Tests `_return_subset`."""
    dictionary = Dictionary({'a': 1, 'b': 2}, default_factory = 7)
    subset = {'a': 1}
    result = utilities._return_subset(subset, dictionary, 'class')
    assert isinstance(result, Dictionary)
    assert result.contents == subset
    assert result.default_factory is None
    result = utilities._return_subset(subset, dictionary, 'copy')
    assert isinstance(result, Dictionary)
    assert result.contents == subset
    assert result.default_factory == 7
    assert result is not dictionary
    assert dictionary.contents == {'a': 1, 'b': 2}
    assert utilities._return_subset(subset, dictionary, 'simple') is subset
    with pytest.raises(ValueError, match = 'returns argument'):
        utilities._return_subset(subset, dictionary, 'other')  # type: ignore[arg-type]
    assert utilities._return_subset([1], Listing([1, 2]), 'class') == Listing([1])


def test_uniquify() -> None:
    """Tests `_uniquify`."""
    assert utilities._uniquify('key', {}) == 'key'
    assert utilities._uniquify('key', {'other': 1}) == 'key'
    assert utilities._uniquify('key', {'key': 1}) == 'key2'
    assert utilities._uniquify('key', {'key': 1, 'key2': 1}) == 'key3'
    existing = {'key': 1} | {f'key{i}': 1 for i in range(2, 12)}
    assert utilities._uniquify('key', existing) == 'key12'
    assert utilities._uniquify('key', {'key': 1}, index = 4) == 'key5'
