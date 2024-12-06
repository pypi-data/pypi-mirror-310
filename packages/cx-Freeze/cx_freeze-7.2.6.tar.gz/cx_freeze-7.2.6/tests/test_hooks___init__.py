"""Tests for cx_Freeze.hooks."""

from __future__ import annotations

import pytest
from generate_samples import create_package
from cx_Freeze import ConstantsModule, ModuleFinder
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize(
    ("name", "modules", "missing", "maybe_missing", "source"),
    [
        [
            "pathy",
            ["pathy", "os"],
            [],
            [],
            """pathy.py
            import os.path
            print(os.path.join("asd", "xyz"))
            """,
        ],
    ],
    ids=["ignore_os_path"],
)
def test_using_finder(
    tmp_path: Path,
    name: str,
    modules: list[str],
    missing,
    maybe_missing,
    source: str,
) -> None:
    """Provides test cases for ModuleFinder class."""
    create_package(tmp_path, source)
    finder = ModuleFinder(ConstantsModule())
    # finder.include_module(import_this)
    finder.include_file_as_module(tmp_path.joinpath(name).with_suffix(".py"))
    # if report:
    #    finder.report_missing_modules()
    found = set([module.name for module in finder.modules])
    # check if we found at least what we expected
    assert found.issuperset(modules)
