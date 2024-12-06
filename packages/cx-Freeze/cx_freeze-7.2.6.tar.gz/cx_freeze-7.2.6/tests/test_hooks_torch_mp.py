"""Tests for torch.multiprocessing."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from generate_samples import create_package, run_command

from cx_Freeze._compat import BUILD_EXE_DIR, EXE_SUFFIX

if TYPE_CHECKING:
    from pathlib import Path

pytest.importorskip("torch", reason="Depends on extra package: torch")

SOURCE_MP = """\
test.py
    import torch
    from multiprocessing import freeze_support

    def per_device_launch_fn(current_gpu_index, num_gpu):
        for i in range(1, 1000):
            print(f"Hello from cx_Freeze #{i}")

    if __name__ == "__main__":
        freeze_support()
        torch.multiprocessing.start_processes(
            per_device_launch_fn,
            args=(num_gpu,),
            nprocs=num_gpu,
            join=True,
            start_method="spawn",
        )
command
    cxfreeze --script test.py build_exe --excludes=tkinter --silent
"""


def test_torch_mp(tmp_path: Path) -> None:
    """Provides test cases for torch.multiprocessing."""
    create_package(tmp_path, SOURCE_MP)
    output = run_command(tmp_path)
    target_dir = tmp_path / BUILD_EXE_DIR
    executable = target_dir / f"test{EXE_SUFFIX}"
    assert executable.is_file()
    output = run_command(target_dir, executable, timeout=10)
    assert output.splitlines()[-1].startswith("Hello from cx_Freeze #")
