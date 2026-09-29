"""Tests for the package namespace."""

from __future__ import annotations

import pathlib
import re

import bunches


def test_all_exports() -> None:
    """Tests that everything in `__all__` is importable."""
    for name in bunches.__all__:
        assert hasattr(bunches, name)
    assert set(bunches.__all__) == {
        'Bunch', 'Catalog', 'ChainDict', 'DictList', 'Dictionary', 'Listing',
        'Repository'}


def test_metadata() -> None:
    """Tests package metadata."""
    assert re.fullmatch(r'\d+\.\d+\.\d+.*', bunches.__version__)
    assert bunches.__author__ == 'Corey Rayburn Yung'


def test_python_requirement() -> None:
    """Tests that pyproject.toml requires Python 3.11 or later."""
    path = pathlib.Path(__file__).parents[1] / 'pyproject.toml'
    text = path.read_text(encoding = 'utf-8')
    assert 'requires-python = ">=3.11"' in text
    assert 'Python :: 3.10' not in text
