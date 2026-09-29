"""Shared fixtures and helper classes for unit tests."""

from __future__ import annotations

import dataclasses
from collections.abc import Iterator

import pytest

from bunches import settings


@dataclasses.dataclass
class Something:
    """Item with a `name` attribute."""

    name: str = 'something'


@dataclasses.dataclass
class Another:
    """Item with a different `name` attribute."""

    name: str = 'another'


class Unnamed:
    """Item without a `name` attribute."""


@pytest.fixture(autouse = True)
def _reset_settings() -> Iterator[None]:
    """Restores the global settings after each test."""
    namer = settings._KEY_NAMER
    method_namer = settings._METHOD_NAMER
    subset_return = settings._SUBSET_RETURN
    yield
    settings._KEY_NAMER = namer
    settings._METHOD_NAMER = method_namer
    settings._SUBSET_RETURN = subset_return
