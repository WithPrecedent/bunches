# Changelog

All notable changes to this project will be documented in this file.

<!-- insertion marker -->

## 0.3.0

* **Breaking:** `ChainDict.parents` is now a property, as in `collections.ChainMap`. Use `chain.parents` instead of `chain.parents()`
* **Breaking:** removed `settings.set_method_namer` and `settings._METHOD_NAMER`, which nothing used, along with the unused `kinds.GenericSet` and `kinds._MISSING` sentinel
* **Breaking:** `DictList.subset` now selects items by name (as `DictList` indexing, `get` and `delete` do) instead of by equality
* `in` now only checks a mapping's stored keys, so the `all`, `default` and `none` wildcards are no longer always "in" a `Catalog`, and a list of keys is never "in" one. `ChainDict` checks each stored mapping
* `subset` now returns deep copies of the selected values whether `include`, `exclude` or both are passed. Before, values chosen with `include` were shared with the original
* Updated `astral-sh/setup-uv` to 10.3.1 and the locked `markdown-exec`, `mkdocs-coverage`, `mypy`, `pre-commit`, `ruff` and `uv` versions (replacing the open Dependabot pull requests), and the `ruff` and `uv` `pre-commit` hooks to match
* Restyled the README examples (single quotes and spaces around keyword argument `=`)
* Added a `py.typed` marker so that type checkers (such as `mypy` in `bobbie`) use the package's type hints
* Fixed the `mypy` error from the `__delitem__` signatures of `Bunch` and `MutableSequence` disagreeing
* `Dictionary.fromkeys` and `ChainDict.fromkeys` now accept any iterable of keys and default `value` to `None`, as `dict.fromkeys` does
* Fixed `Catalog` lookups and `Catalog.delete` with a `tuple` that is itself a stored key, which were treated as a sequence of separate keys
* `ChainDict.new_child` now accepts a plain mapping (wrapped in a `Dictionary`, as `add` does) or no mapping (an empty `Dictionary`), as `collections.ChainMap.new_child` does
* Fixed `Repository.add` ignoring an empty `str` key
* `Repository.add` now raises a `ValueError` when no key is passed and the key namer cannot name the item, instead of storing it under `None`
* Fixed unique key suffixes when `_uniquify` starts from an `index` other than 1
* `ChainDict.return_first` and `Repository.overwrite` are now typed as `bool` instead of `bool | None`
* Updated to the `snickerdoodle` 0.5.0 template (Codecov coverage, a coverage page in the docs, Python 3.15, SPDX license metadata, the version read from `__version__`, GitHub CLI releases, and CI that runs `mypy` and `pre-commit` once). Added `.cruft.json` so that `cruft update` can apply future template changes
* Replaced the misnamed `,python-version` file with `.python-version` and converted the files with Windows line endings to Unix line endings
* Ruff now enforces single quotes and the 80 character line limit, and its `force-exclude` setting keeps `pre-commit` from linting the excluded folders
* Restyled the package and tests (spaces around keyword argument `=`, closing brackets on the last line, `Public Methods` section markers, and complete docstrings with `Returns` before `Raises`)
* Fixed the changelog entries, which were indented so that Markdown showed them as code
* Added tests for the fixes above, the `+` and `+=` operators of every class, `tuple` keys, `ChainDict.get`, the `py.typed` marker, and more (149 tests in total)

## 0.2.2

* Updated to the `snickerdoodle` 0.4.0 template
* Removed `ruff format` from the `pre-commit` hooks because it removes the spaces around "=" in keyword arguments
* Made `ruff` prefer single quotes and converted the strings in the code to single quotes
* Made `ruff` ignore boolean default positional arguments (`FBT002`)
* Relaxed `pydoclint` checks of type hints, class attributes, and raised exceptions
* Excluded `uv.lock` from the large file check
* Fixed typos in the contributing guide and noted that the project does not use a code formatter

## 0.2.1

* Fixed CI: applied pre-commit formatting, configured `pydoclint`, fixed `dependabot`
* README examples now show results as comments instead of `>>>` prompts

## 0.2.0

* Updated to the latest `snickerdoodle` template: `uv` and `hatchling` replace `pdm`, new GitHub Actions, pre-commit, codecov, and mkdocs configuration
* Dropped support for Python 3.10 (Python 3.11 and later are supported)
* `Bunch.__add__` (`+`) now returns a modified copy instead of modifying the instance; use `+=` to modify in place
* `Bunch.__delitem__` now returns `None`
* `subset` methods take `returns = None`, which reads `settings._SUBSET_RETURN` at call time so `settings.set_subset_return` (new) takes effect; `Listing.subset` and `DictList.subset` gained the `returns` argument
* `settings.set_key_namer` now works and is used by `Repository` and `DictList`; added `settings.set_subset_return`
* `ChainDict`: fixed `return_first = False` results, iteration and `len` now use keys, `add` wraps plain mappings, `subset` ignores keys missing from a stored mapping, `delete` raises `KeyError` for missing keys, `parents` keeps `return_first`
* `Catalog.delete` modifies `contents` in place
* `DictList`: `get` handles out-of-range indices, slices are supported, multiple matches return a `DictList`, `delete` raises `KeyError` when nothing matches
* `Listing.prepend` no longer flattens nested sequences; `bytes` are appended, not extended
* Completed README, docs, and docstrings; added a full unit test suite

## 0.1.3

* Added `pynguin` to test dependencies

## 0.1.2

* Fixed ruff error in `ci.yaml`
* Removed unneeded actions

## 0.1.1

* Reduced to core classes
* Adapted to `snickerdoodle` template

## 0.1.0

* Initial Commit
