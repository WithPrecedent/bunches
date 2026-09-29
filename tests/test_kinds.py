"""Tests for `bunches.kinds`."""

from __future__ import annotations

import typing

from bunches import kinds


def test_subset_returns() -> None:
    """Tests the options in `SubsetReturns`."""
    assert typing.get_args(kinds.SubsetReturns) == ('class', 'copy', 'simple')


def test_aliases() -> None:
    """Tests that type aliases exist."""
    assert kinds.GenericDict is not None
    assert kinds.GenericList is not None
    assert kinds.GenericSet is not None


def test_missing() -> None:
    """Tests the missing value sentinel."""
    assert isinstance(kinds._MISSING, kinds._MISSING_VALUE)
    assert kinds._MISSING is not None
    assert kinds._MISSING == kinds._MISSING_VALUE()
