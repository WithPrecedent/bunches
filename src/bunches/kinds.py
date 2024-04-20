"""Types and type aliases for the package.

Contents:


To Do:


"""
from __future__ import annotations

import dataclasses
import sys
from collections.abc import Hashable, MutableMapping, MutableSequence
from collections.abc import Set as AbstractSet
from typing import Any, Literal, TypeAlias

if sys.version_info < (3, 12):
    GenericDict: TypeAlias = MutableMapping[Hashable, Any]
    GenericList: TypeAlias = MutableSequence[Any]
    GenericSet: TypeAlias = AbstractSet[Any]
    SubsetReturns: TypeAlias = Literal['class', 'copy', 'simple']
else:
    type GenericDict = MutableMapping[Hashable, Any]
    type GenericList = MutableSequence[Any]
    type GenericSet = AbstractSet[Any]
    type SubsetReturns = Literal['class', 'copy', 'simple']


@dataclasses.dataclass
class _MISSING_VALUE:  # noqa: N801
    """Sentinel object for a missing data or parameter.

    This follows the same pattern as the `_MISSING_TYPE` class in the builtin
    dataclasses library.
    https://github.com/python/cpython/blob/3.10/Lib/dataclasses.py#L182-L186

    Because None is sometimes a valid argument or data option, this class
    provides an alternative that does not create the confusion that a default of
    None can sometimes lead to.

    """

    pass  # noqa: PIE790


# _MISSING, instance of MISSING_VALUE, should be used for missing values as an
# alternative to None. This provides a fuller repr and traceback.
_MISSING = _MISSING_VALUE()
