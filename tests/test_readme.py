"""Tests that every example in the README works as documented.

Code blocks in the README show results as trailing comments (for example,
`colors.get('purple')  # 0`). This test runs each block and checks that every
expression with such a comment evaluates to the value shown.
"""

from __future__ import annotations

import ast
import pathlib
import re
import sys
import types

README = pathlib.Path(__file__).parents[1] / 'README.md'
_RESULT = re.compile(r'\s{2}# (?P<expected>.+)$')


def test_readme_examples() -> None:
    """Runs all of the python code blocks in the README."""
    text = README.read_text(encoding = 'utf-8')
    blocks = re.findall(r'```python\n(.*?)```', text, flags = re.DOTALL)
    assert blocks
    module = types.ModuleType('readme')
    sys.modules['readme'] = module
    namespace = module.__dict__
    checked = 0
    try:
        checked = _run(blocks, namespace)
    finally:
        del sys.modules['readme']
    assert checked > 20


def _run(blocks: list[str], namespace: dict[str, object]) -> int:
    """Runs code blocks and checks results shown in comments.

    Args:
        blocks: source code of the README code blocks.
        namespace: namespace shared by all of the blocks.

    Returns:
        Number of results checked.

    """
    checked = 0
    for block in blocks:
        lines = block.splitlines()
        for node in ast.parse(block).body:
            if isinstance(node, ast.Expr):
                match = _RESULT.search(lines[node.end_lineno - 1])
                if match:
                    code = compile(ast.Expression(node.value), 'README', 'eval')
                    result = eval(code, namespace)  # noqa: S307
                    assert repr(result) == match['expected']
                    checked += 1
                    continue
            module = ast.Module(body = [node], type_ignores = [])
            exec(compile(module, 'README', 'exec'), namespace)  # noqa: S102
    return checked
