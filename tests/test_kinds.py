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


def test_removed_members() -> None:
    """Tests that unused members were removed."""
    assert not hasattr(kinds, 'GenericSet')
    assert not hasattr(kinds, '_MISSING')
