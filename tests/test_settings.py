"""Tests for `bunches.settings`."""

from __future__ import annotations

import pytest

from bunches import Dictionary, DictList, Listing, Repository, settings


def test_defaults() -> None:
    """Tests the default global values."""
    assert 'all' in settings._ALL_KEYS
    assert 'default' in settings._DEFAULT_KEYS
    assert 'none' in settings._NONE_KEYS
    assert settings._SUBSET_RETURN == 'class'
    assert settings._KEY_NAMER('Item') == 'Item'
    assert settings._METHOD_NAMER('Item') == 'from_Item'


def test_set_key_namer() -> None:
    """Tests `set_key_namer`, including its effect on other classes."""
    settings.set_key_namer(lambda item: str(item).upper())
    assert settings._KEY_NAMER('a') == 'A'
    repository = Repository()
    repository.add('b')
    assert repository.keys() == ('B',)
    assert DictList(['x', 'y']).keys() == ('X', 'Y')
    assert DictList(['x', 'y'])['Y'] == 'y'
    with pytest.raises(TypeError):
        settings.set_key_namer('not callable')  # type: ignore[arg-type]


def test_set_method_namer() -> None:
    """Tests `set_method_namer`."""
    settings.set_method_namer(lambda item: f'make_{item}')
    assert settings._METHOD_NAMER('x') == 'make_x'
    with pytest.raises(TypeError):
        settings.set_method_namer(3)  # type: ignore[arg-type]


def test_set_subset_return() -> None:
    """Tests `set_subset_return`, including its effect on `subset` methods."""
    settings.set_subset_return('simple')
    assert Dictionary({'a': 1, 'b': 2}).subset(include = 'a') == {'a': 1}
    assert Listing([1, 2, 3]).subset(include = [1, 2]) == [1, 2]
    settings.set_subset_return('copy')
    assert isinstance(Listing([1]).subset(exclude = 2), Listing)
    with pytest.raises(ValueError, match = 'returns argument'):
        settings.set_subset_return('other')  # type: ignore[arg-type]
    assert settings._SUBSET_RETURN == 'copy'
