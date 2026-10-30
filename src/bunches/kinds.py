"""Types and type aliases for the package.

Contents:
    GenericDict: type alias for any mutable mapping with hashable keys.
    GenericList: type alias for any mutable sequence.
    SubsetReturns: type alias for the options of the `returns` argument of
        `subset` methods.

"""

from __future__ import annotations

from collections.abc import Hashable, MutableMapping, MutableSequence
from typing import Any, Literal, TypeAlias

""" Type Aliases """

GenericDict: TypeAlias = MutableMapping[Hashable, Any]
GenericList: TypeAlias = MutableSequence[Any]
SubsetReturns: TypeAlias = Literal['class', 'copy', 'simple']
