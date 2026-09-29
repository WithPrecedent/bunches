# Changelog

All notable changes to this project will be documented in this file.

<!-- insertion marker -->

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
