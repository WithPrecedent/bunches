# bunches

| | |
| --- | --- |
| Version | [![PyPI Latest Release](https://img.shields.io/pypi/v/bunches.svg?style=for-the-badge&color=steelblue&label=PyPI&logo=PyPI&logoColor=yellow)](https://pypi.org/project/bunches/) [![GitHub Latest Release](https://img.shields.io/github/v/tag/WithPrecedent/bunches?style=for-the-badge&color=navy&label=GitHub&logo=github)](https://github.com/WithPrecedent/bunches/releases)
| Status | [![Build Status](https://img.shields.io/github/actions/workflow/status/WithPrecedent/bunches/ci.yml?branch=main&style=for-the-badge&color=cadetblue&label=Tests&logo=pytest)](https://github.com/WithPrecedent/bunches/actions/workflows/ci.yml?query=branch%3Amain) [![Development Status](https://img.shields.io/badge/Development-Active-seagreen?style=for-the-badge&logo=git)](https://www.repostatus.org/#active) [![Project Stability](https://img.shields.io/pypi/status/bunches?style=for-the-badge&logo=pypi&label=Stability&logoColor=yellow)](https://pypi.org/project/bunches/)
| Documentation | [![Hosted By](https://img.shields.io/badge/Hosted_by-Github_Pages-blue?style=for-the-badge&color=navy&logo=github)](https://WithPrecedent.github.io/bunches)
| Tools | [![Documentation](https://img.shields.io/badge/MkDocs-magenta?style=for-the-badge&color=deepskyblue&logo=markdown&labelColor=gray)](https://squidfunk.github.io/mkdocs-material/) [![Linter](https://img.shields.io/endpoint?style=for-the-badge&url=https://raw.githubusercontent.com/charliermarsh/Ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/Ruff) [![Dependency Manager](https://img.shields.io/badge/PDM-mediumpurple?style=for-the-badge&logo=affinity&labelColor=gray)](https://PDM.fming.dev) [![Pre-commit](https://img.shields.io/badge/pre--commit-darkolivegreen?style=for-the-badge&logo=pre-commit&logoColor=white&labelColor=gray)](https://github.com/TezRomacH/python-package-template/blob/master/.pre-commit-config.yaml) [![CI](https://img.shields.io/badge/GitHub_Actions-navy?style=for-the-badge&logo=githubactions&labelColor=gray&logoColor=white)](https://github.com/features/actions) [![Editor Settings](https://img.shields.io/badge/Editor_Config-paleturquoise?style=for-the-badge&logo=editorconfig&labelColor=gray)](https://editorconfig.org/) [![Repository Template](https://img.shields.io/badge/snickerdoodle-bisque?style=for-the-badge&logo=cookiecutter&labelColor=gray)](https://www.github.com/WithPrecedent/bunches) [![Dependency Maintainer](https://img.shields.io/badge/dependabot-navy?style=for-the-badge&logo=dependabot&logoColor=white&labelColor=gray)](https://github.com/dependabot)
| Compatibility | [![Compatible Python Versions](https://img.shields.io/pypi/pyversions/bunches?style=for-the-badge&color=steelblue&label=Python&logo=python&logoColor=yellow)](https://pypi.python.org/pypi/bunches/) [![Linux](https://img.shields.io/badge/Linux-lightseagreen?style=for-the-badge&logo=linux&labelColor=gray&logoColor=white)](https://www.linux.org/) [![MacOS](https://img.shields.io/badge/MacOS-snow?style=for-the-badge&logo=apple&labelColor=gray)](https://www.apple.com/macos/) [![Windows](https://img.shields.io/badge/windows-blue?style=for-the-badge&logo=Windows&labelColor=gray&color=orangered)](https://www.microsoft.com/en-us/windows?r=1)
| Stats | [![PyPI Download Rate (per month)](https://img.shields.io/pypi/dm/bunches?style=for-the-badge&color=steelblue&label=Downloads%20💾&logo=pypi&logoColor=yellow)](https://pypi.org/project/bunches) [![GitHub Stars](https://img.shields.io/github/stars/WithPrecedent/bunches?style=for-the-badge&color=navy&label=Stars%20⭐&logo=github)](https://github.com/WithPrecedent/bunches/stargazers) [![GitHub Contributors](https://img.shields.io/github/contributors/WithPrecedent/bunches?style=for-the-badge&color=navy&label=Contributors%20🙋&logo=github)](https://github.com/WithPrecedent/bunches/graphs/contributors) [![GitHub Issues](https://img.shields.io/github/issues/WithPrecedent/bunches?style=for-the-badge&color=navy&label=Issues%20📘&logo=github)](https://github.com/WithPrecedent/bunches/graphs/contributors) [![GitHub Forks](https://img.shields.io/github/forks/WithPrecedent/bunches?style=for-the-badge&color=navy&label=Forks%20🍴&logo=github)](https://github.com/WithPrecedent/bunches/forks)
| | |

-----

## What is bunches?

[TODO: Brief summary of the project]

## Why use bunches?

## Mappings

* `Dictionary`: drop-in replacement for a python dict with an `add` method for a default mechanism of adding data, a `delete` method for a default mechanism of deleting data, and a `subset` method for returning a subset of the key/value pairs in a new `Dictionary`.
* `Catalog`: wildcard-accepting dict which is intended for storing different options and strategies. It also returns lists of matches if a list of keys is provided.
* `Library`: a dictionary that automatically supplies key names for stored items. The 'overwrite' argument determines if a unique key should always be created or whether entries may be overwritten.

### Sequences

* `Listing`: drop-in replacement for a python list with an `add` method for a default mechanism of adding data, a `delete` method for a default mechanism of deleting data, and a `subset` method for returning a subset of the key/value pairs in a new `Listing`.
* `DictList`: iterable with both dict and list interfaces. Stored items must be hashable or have a `name` attribute.

## Getting started

### Requirements

[TODO: List any OS or other restrictions and pre-installation dependencies]

### Installation

To install `bunches`, use `pip`:

```sh
pip install bunches
```

### Usage

[TODO: Describe common use cases, with possible example(s)]

## Contributing

Contributors are always welcome. Feel free to grab an [issue](https://www.github.com/WithPrecedent/bunches/issues) to work on or make a suggested improvement. If you wish to contribute, please read the [Contribution Guide](https://www.github.com/WithPrecedent/bunches/contributing.md) and [Code of Conduct](https://www.github.com/WithPrecedent/bunches/code_of_conduct.md).

## Similar Projects

[TODO: If they exist, it is always nice to acknowledge other similar efforts]

## Acknowledgments

I'd also like to extend a special thanks to [pawamoy](https://github.com/pawamoy) whose excellent `pdm` and `mkdocs` extensions and utlities are incorporated into `snickerdoodle`. Some of the scripts, documentation, configuration files, and other CI code were all adapted from pawamoy's repositories.

I would also like to thank the University of Kansas School of Law for tolerating and supporting this law professor's coding efforts, an endeavor which is well outside the typical scholarly activities in the discipline.

## License

Use of this repository is authorized under the [Apache Software License 2.0](https://www.github.com/WithPrecedent/bunches/blog/main/LICENSE).
