"""Tests for `bunches.settings`."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from bunches import DictList, Dictionary, Listing, Repository, settings

if TYPE_CHECKING:
    from bunches.kinds import SubsetReturns


def test_defaults() -> None:
    """Tests the default global values."""
    assert 'all' in settings._ALL_KEYS
    assert 'default' in settings._DEFAULT_KEYS
    assert 'none' in settings._NONE_KEYS
    assert settings._SUBSET_RETURN == 'class'
    assert settings._KEY_NAMER('Item') == 'Item'


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


@pytest.mark.parametrize('returns', ['class', 'copy', 'simple'])
def test_set_subset_return_options(returns: SubsetReturns) -> None:
    """Tests that `set_subset_return` accepts each option.

    Args:
        returns: option to set.

    """
    settings.set_subset_return(returns)
    assert settings._SUBSET_RETURN == returns


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


def test_method_namer_removed() -> None:
    """Tests that the unused method namer was removed."""
    assert not hasattr(settings, 'set_method_namer')
    assert not hasattr(settings, '_METHOD_NAMER')
