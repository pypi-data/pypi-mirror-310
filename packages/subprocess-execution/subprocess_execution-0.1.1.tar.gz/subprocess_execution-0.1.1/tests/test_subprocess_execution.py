import ctypes
import subprocess
from typing import Set

import pytest
from pytest import CaptureFixture

from subprocess_execution import run_in_subprocess


def list_shared_memory_segments() -> Set[str]:
    """List shared memory segments using ipcs command."""
    result = subprocess.run(["ipcs", "-m"], capture_output=True, text=True)
    output = result.stdout
    segments = {line.split()[1] for line in output.splitlines() if "0x" in line}
    return segments


def test_run_in_subprocess_basic() -> None:
    @run_in_subprocess()
    def add(x: int, y: int) -> int:
        return x + y

    result = add(3, 4)
    assert result == 7


def test_run_in_subprocess_exception() -> None:
    @run_in_subprocess()
    def raise_exception() -> None:
        raise ValueError("This is an error!")

    with pytest.raises(Exception, match="Error in subprocess: This is an error!"):
        raise_exception()


def test_run_in_subprocess_crash() -> None:
    @run_in_subprocess()
    def crash() -> None:
        p = ctypes.pointer(ctypes.c_char.from_address(5))
        p[0] = b"x"

    with pytest.raises(
        Exception,
        match="Error: Subprocess terminated unexpectedly with return code -11.",
    ):
        crash()


def test_run_in_subprocess_stdout(capfd: CaptureFixture[str]) -> None:
    @run_in_subprocess()
    def print_test() -> None:
        print("Test print!")

    result = print_test()
    captured = capfd.readouterr()  # Read captured stdout and stderr

    assert captured.out == "Test print!\n"
    assert result is None  # As print_test does not return anything.


def test_timeout() -> None:
    @run_in_subprocess(timeout_seconds=2)
    def timeout_function() -> None:
        while True:
            continue

    with pytest.raises(Exception, match="Error: The subprocess has timed out."):
        timeout_function()


def time_timeout_pipe_output(capfd: CaptureFixture[str]) -> None:
    @run_in_subprocess(timeout_seconds=2)
    def timeout_print_function() -> None:
        print("Test print!")
        while True:
            continue

    with pytest.raises(Exception, match="Error: The subprocess has timed out."):
        timeout_print_function()
        captured = capfd.readouterr()
        assert captured.out == "Test print!\n"


def test_run_subprocess_exit() -> None:
    @run_in_subprocess()
    def call_exit() -> None:
        exit(0)

    # get list of shm prior to function call.
    prior_shm_names = list_shared_memory_segments()
    # No output shared memory should exsist, child killed early.
    with pytest.raises(
        Exception, match="Error in subprocess: No, output result found in shm."
    ):
        call_exit()
    post_shm_names = list_shared_memory_segments()
    assert prior_shm_names == post_shm_names


def test_cleanup_shared_memory() -> None:
    @run_in_subprocess()
    def simple_function() -> str:
        return "Simple!"

    # get list of shm prior to function call.
    prior_shm_names = list_shared_memory_segments()
    simple_function()
    post_shm_names = list_shared_memory_segments()
    assert prior_shm_names == post_shm_names
