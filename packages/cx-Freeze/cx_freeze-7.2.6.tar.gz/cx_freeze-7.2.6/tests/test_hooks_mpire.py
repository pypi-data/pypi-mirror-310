"""Tests for mpire."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

import pytest
from generate_samples import create_package, run_command

from cx_Freeze._compat import BUILD_EXE_DIR, EXE_SUFFIX

if TYPE_CHECKING:
    from pathlib import Path

pytest.importorskip("mpire", reason="Depends on extra package: mpire")

SOURCE = """\
sample0.py
    from multiprocessing import freeze_support

    def foo(n):
        return f"Hello from cx_Freeze #{n}"

    if __name__ == "__main__":
        freeze_support()
        from mpire import WorkerPool
        with WorkerPool(2, start_method='spawn') as pool:
            results = pool.map(foo, range(10))
        for line in sorted(results):
            print(line)
setup.py
    from cx_Freeze import setup
    setup(
        name="test_mpire",
        version="0.1",
        description="Sample for test with cx_Freeze",
        executables=["sample0.py"],
        options={
            "build_exe": {
                "excludes": ["tkinter"],
                "silent": True,
            }
        }
    )
"""
EXPECTED_OUTPUT = [
    "Hello from cx_Freeze #9",
]


def _parameters_data() -> Iterator:
    import multiprocessing as mp

    methods = mp.get_all_start_methods()
    for method in methods:
        source = SOURCE.replace("='spawn'", f"='{method}'")
        for i, expected in enumerate(EXPECTED_OUTPUT):
            if method == "forkserver" and i != 3:
                continue  # only sample3 works with forkserver method
            sample = f"sample{i}"
            test_id = f"{sample}-{method}"
            yield pytest.param(source, sample, expected, id=test_id)


@pytest.mark.parametrize(("source", "sample", "expected"), _parameters_data())
def test_mpire(
    tmp_path: Path, source: str, sample: str, expected: str
) -> None:
    """Provides test cases for mpire."""
    create_package(tmp_path, source)
    output = run_command(tmp_path)
    target_dir = tmp_path / BUILD_EXE_DIR
    executable = target_dir / f"{sample}{EXE_SUFFIX}"
    assert executable.is_file()
    output = run_command(target_dir, executable, timeout=10)
    assert output.splitlines()[-1] == expected
