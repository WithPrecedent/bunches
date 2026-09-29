"""Types and type aliases for the package.

Contents:
    GenericDict: type alias for any mutable mapping with hashable keys.
    GenericList: type alias for any mutable sequence.
    GenericSet: type alias for any set.
    SubsetReturns: type alias for the options of the `returns` argument of
        `subset` methods.
    _MISSING_VALUE: type of the sentinel for missing values.
    _MISSING: sentinel for missing values, used as an alternative to `None`.

"""

from __future__ import annotations

import dataclasses
from collections.abc import Hashable, MutableMapping, MutableSequence
from collections.abc import Set as AbstractSet
from typing import Any, Literal, TypeAlias

GenericDict: TypeAlias = MutableMapping[Hashable, Any]
GenericList: TypeAlias = MutableSequence[Any]
GenericSet: TypeAlias = AbstractSet[Any]
SubsetReturns: TypeAlias = Literal["class", "copy", "simple"]


@dataclasses.dataclass
class _MISSING_VALUE:  # noqa: N801
    """Sentinel object for a missing data or parameter.

    This follows the same pattern as the `_MISSING_TYPE` class in the builtin
    dataclasses library.
    https://github.com/python/cpython/blob/3.11/Lib/dataclasses.py

    Because None is sometimes a valid argument or data option, this class
    provides an alternative that does not create the confusion that a default of
    None can sometimes lead to.

    """

    pass  # noqa: PIE790


# _MISSING, instance of MISSING_VALUE, should be used for missing values as an
# alternative to None. This provides a fuller repr and traceback.
_MISSING = _MISSING_VALUE()
