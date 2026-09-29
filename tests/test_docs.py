"""Tests that the python examples in the documentation run without error."""

from __future__ import annotations

import pathlib
import re
import sys
import types

import pytest

DOCS = pathlib.Path(__file__).parents[1] / 'docs'


@pytest.mark.parametrize('name', ['tutorial', 'advanced', 'recipes'])
def test_doc_examples_run(name: str) -> None:
    """Executes all of the python code blocks of a documentation page."""
    text = (DOCS / f'{name}.md').read_text(encoding = 'utf-8')
    blocks = re.findall(r'```python\n(.*?)```', text, flags = re.DOTALL)
    assert blocks
    module = types.ModuleType(f'docs_{name}')
    sys.modules[module.__name__] = module
    try:
        for block in blocks:
            exec(compile(block, f'{name}.md', 'exec'), module.__dict__)  # noqa: S102
    finally:
        del sys.modules[module.__name__]


def test_documented_results() -> None:
    """Checks a few of the results quoted in the documentation comments."""
    from dataclasses import dataclass

    from bunches import Catalog, ChainDict, DictList, Dictionary, Listing

    colors = Dictionary({'red': 1, 'green': 2}, default_factory = 0)
    colors.add({'blue': 3})
    assert colors.get('purple') == 0
    assert colors.keys() == ('red', 'green', 'blue')
    catalog = Catalog({'tree': 'DecisionTree', 'forest': 'RandomForest'})
    catalog.default = 'forest'
    assert catalog['default'] == 'RandomForest'
    settings = ChainDict([
        Dictionary({'debug': True}),
        Dictionary({'debug': False, 'name': 'app'})])
    settings.return_first = False
    assert settings['debug'] == [True, False]
    assert Listing([1, 2, 3]).subset(exclude = 2, returns = 'simple') == [1, 3]

    @dataclass
    class Step:
        name: str

    pipeline = DictList([Step('load'), Step('clean'), Step('save')])
    pipeline.insert(1, Step('validate'))
    assert pipeline.keys() == ('load', 'validate', 'clean', 'save')
