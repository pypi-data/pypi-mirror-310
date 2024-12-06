from __future__ import annotations

import hashlib
import inspect
import os
import subprocess
import sys
import time
import uuid
from contextlib import contextmanager
from multiprocessing.shared_memory import _make_filename  # type: ignore
from multiprocessing.shared_memory import SharedMemory
from queue import Empty, Queue
from threading import Event, Thread
from typing import IO, Any, Callable, Dict, Iterator, Optional, Tuple

import cloudpickle

FunctionType = Callable[..., Optional[Any]]

DONE_KEY = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
SHARED_MEMORY_KEY = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:8]
RUNNING_KEY = "Function Running!"


def parse_stdout(out: IO[str], queue: Queue[str], stop_event: Event) -> None:
    """Read lines from a file-like output stream, print and inserts into a queue.

    This function runs in a seperate thread, reading lines iteratively from the given
    'out' stream and enqueues them into a given 'queue'. This process is interrupted
    when 'stop_event' is set.

    Args:
        out: File-like object representing the output stream to read from.
        queue: Queue for read lines.
        strop_event: Event that once set will break the loop and stop thread.
    """
    for line in iter(out.readline, b""):
        line_content = line.strip()
        # check if we should stop the thread
        if stop_event.is_set():
            break
        if line_content and line_content != DONE_KEY:
            print(line_content, flush=True)
        queue.put(line)


def print_stderr(out: IO[str], stop_event: Event) -> None:
    """Reads lines from file-like output stream and print to stderr.

    Args:
        out: File-like object representing the output stream to read from.
        stop_event: Event that once set will break the loop and stop the thread.
    """
    for line in iter(out.readline, b""):
        # check if we should stop the thread.
        if stop_event.is_set():
            break
        if line:
            print(line.strip(), file=sys.stderr)


def clear_subprocess_pipes(
    stdout_pipe: Optional[IO[str]] = None, stderr_pipe: Optional[IO[str]] = None
) -> None:
    """Pipe stdout and stderr from child process to parent.

    Args:
        stdout_pipe: IO buffer of stdout from the child process.
        stderr_pipe: IO buffer of stderr from the child process.
    """
    if stdout_pipe is not None:
        for line in stdout_pipe:
            if line:
                print(line.strip())

    if stderr_pipe is not None:
        for line in stderr_pipe:
            if line:
                print(line.strip(), file=sys.stderr)


class ManagedSharedMemory(SharedMemory):
    def __init__(
        self,
        name: Optional[str] = None,
        create: bool = False,
        size: int = 0,
        *,
        deallocate: bool = False,
    ):
        """Initalise ManagedSharedMemory.

        Args:
            name: Name of the shared memory object.
            create: If true, create new shared memory segment.
            size: Size of the shared memory segment.
            deallocate: If true, deallocate memory on close.
        """
        self._managed_name = _make_filename().split("/")[1] if name is None else name
        self._create = create
        self._size = size
        self._deallocate = deallocate

        super().__init__(
            name=self._managed_name + "_sub",
            create=self._create,
            size=self._size,
        )

    @property
    def managed_name(self) -> str:
        """Name of the shared memory object."""
        return self._managed_name

    def close_shm(self) -> None:
        """Close the shared memory and optionally deallocate it."""
        self.close()
        if self._deallocate:
            self.unlink()


@contextmanager
def shared_memory_context(
    size: int = 0,
    name: Optional[str] = None,
    create: bool = False,
    deallocate: bool = True,
) -> Iterator[ManagedSharedMemory]:
    """Context manager for managing the lifecycle of inter-process shared memory.

    Context manager creates or accesses a block of shared memory.

    This context manager is designed to alter the behavior of the multiprocessing
    resource tracker with regard to shared memory management to resolve
    (https://bugs.python.org/issue38119).

    Args:
        size: Size of the shared memory block in bytes.
        name: Name of the shared memory block. If None, unqiue name will be generated.
        create: If true, a new shared memory block is created.
            If false, an attempt is made to access and exsisting block.
        deallocate: If true, the shared memory object will be deallocated on exit of
            the context.

    Note: If deallocate=False the user will be resonsible for dellocating the memory.
        This could persist after the python iterpreter is killed.

    Raises:
        RuntimeError: If the shared memory block is unable to be created or attached.

    Returns:
        shared memory object.
    """

    def patch_resource_tracker() -> None:
        """Patch multiprocessing.resource_tracker (ManagedSharedMemory not tracked).

        https://bugs.python.org/issue38119
        """
        from multiprocessing import resource_tracker
        from typing import Any, Sized  # noqa: F811

        def is_managed_shm(name: str) -> bool:
            return name.split("_")[-1] == "sub"

        def fix_register(name: Sized, rtype: Any) -> None:
            if rtype == "shared_memory" and is_managed_shm(str(name)):
                return
            return resource_tracker._resource_tracker.register(
                self, name, rtype  # type: ignore # noqa: F821
            )

        resource_tracker.register = fix_register

        def fix_unregister(name: Sized, rtype: Any) -> Any:
            if rtype == "shared_memory" and is_managed_shm(str(name)):
                return
            return resource_tracker.unregister(
                self, name, rtype  # type: ignore # noqa: F821
            )

        resource_tracker.unregister = fix_unregister

        if "shared_memory" in resource_tracker._CLEANUP_FUNCS:  # type: ignore
            del resource_tracker._CLEANUP_FUNCS["shared_memory"]  # type: ignore

    patch_resource_tracker()

    shm = None
    try:
        shm = ManagedSharedMemory(
            name=name,
            size=size,
            create=create,
            deallocate=deallocate,
        )
    except FileNotFoundError:
        # raise if create=False and file handle to existing shm is not found.
        raise RuntimeError(f"Could not attach to shared memory {name}.")
    except FileExistsError:
        # raise if create=True and shm already exsists.
        raise RuntimeError(
            f"Could not create the shared memory {name} as already exsists."
        )
    else:
        yield shm
    finally:
        # close and unlink the shared memory.
        if shm is not None:
            shm.close_shm()


shm_context_code = inspect.getsource(shared_memory_context)
managed_shm_code = inspect.getsource(ManagedSharedMemory)


def run_in_subprocess(
    timeout_seconds: Optional[int] = None,
) -> Callable[[FunctionType], FunctionType]:
    """Decorator factory to execute function in a new subprocess.

    This decorator serializes the function, its arguments and keyword arguments
    using cloudpickle. The serialized data is then passed to a subprocess via
    shared memory and executed within the subprocess. Any results (or errors) are
    serialized and returned to the parent process.

    Args:
        timeout_seconds: Maximum number of seconds the to allow for execution within
            subprocess before being terminated. If None, no timeout is enforced.

    Returns:
        A wrapped version of func that, when called, executes func within a subprocess
        and returns the result.

    Raises:
        Exception: If the function execution in the subprocess results in an error.

    Examples:
        No timeout:
        @run_in_subprocess()
        def some_function(arg1, arg2):
            return arg1 + arg2

        With 300s timeout.
        @run_in_subprocess(timeout_seconds=300)
        def some_function(arg1, arg2):
            return arg1 + arg2
    """

    def run_subprocess(func: FunctionType) -> FunctionType:
        def subprocess_code(in_shm_name: str, out_shm_name: str) -> str:
            return f"""
import io
import sys
from contextlib import contextmanager
from multiprocessing import shared_memory
from multiprocessing.shared_memory import SharedMemory
from typing import Iterator, Optional, ContextManager

import cloudpickle

{managed_shm_code}
{shm_context_code}

with shared_memory_context(
    name='{in_shm_name}', create=False, deallocate=False
) as input_shm:
    serialized_data = input_shm.buf.tobytes()
    func, args, kwargs = cloudpickle.loads(serialized_data)

try:
    result = func(*args, **kwargs)
    serialized_result = cloudpickle.dumps(('success', result))
except Exception as e:
    serialized_result = cloudpickle.dumps(('error', str(e)))

with shared_memory_context(
    name="{out_shm_name}",
    create=True,
    size=len(serialized_result) + 1,
    deallocate=False,
) as shm_result:

    # The first byte is the "signal" byte. If it's set to 1, we terminate.
    shm_result.buf[0] = 0
    shm_result.buf[1:len(serialized_result) + 1] = serialized_result
    sys.stdout.write(f"{DONE_KEY}" + '\\n')
    sys.stdout.flush()

    while True:
        if shm_result.buf[0] == 1:
            break

"""

        def wrapper(*args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Optional[Any]:
            data = (func, args, kwargs)
            serialized_data = cloudpickle.dumps(data)

            # create shared memory and write the serialized data.
            with shared_memory_context(
                create=True,
                size=len(serialized_data),
                deallocate=True,
            ) as input_shm:
                input_shm.buf[: len(serialized_data)] = serialized_data
                # Create name for output shm.
                out_shm_name = _make_filename().split("/")[1]

                cmd = [
                    sys.executable,
                    "-c",
                    subprocess_code(input_shm.managed_name, out_shm_name),
                ]

                proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    env=dict(os.environ, PYTHONUNBUFFERED="1"),
                )

                queue: Queue[str] = Queue()
                stop_event = Event()

                thread_stdout = Thread(
                    target=parse_stdout, args=(proc.stdout, queue, stop_event)
                )
                thread_stderr = Thread(
                    target=print_stderr, args=(proc.stderr, stop_event)
                )
                thread_stdout.daemon = True
                thread_stderr.daemon = True
                thread_stdout.start()
                thread_stderr.start()

                start_time = time.time()

                while True:
                    # non-blocking read from stdout.
                    try:
                        status = queue.get_nowait()
                    except Empty:
                        # No stdout: function still running with no current stdout.
                        status = RUNNING_KEY

                    if status:
                        if status.strip() == DONE_KEY:
                            # subprocess execution complete.
                            break
                    else:
                        # Empty string: subprocess has closed stdout.
                        break

                    if timeout_seconds:
                        # check for timeout or subprocess termination.
                        elapsed_time = time.time() - start_time
                        if elapsed_time > timeout_seconds:
                            stop_event.set()
                            proc.terminate()
                            thread_stdout.join()
                            thread_stderr.join()
                            clear_subprocess_pipes(proc.stdout, proc.stderr)
                            raise Exception("Error: The subprocess has timed out.")

                    time.sleep(0.1)  # sleep for short duration.

                # check if the subprocess has crashed.
                if proc.poll() is not None and proc.returncode != 0:
                    # maybe grab the stacktrace?
                    stop_event.set()
                    thread_stdout.join()
                    thread_stderr.join()
                    clear_subprocess_pipes(proc.stdout, proc.stderr)
                    raise Exception(
                        f"Error: Subprocess terminated unexpectedly with "
                        f"return code {proc.returncode}."
                    )

                # try and read result from shared memory.
                try:
                    with shared_memory_context(
                        name=out_shm_name, deallocate=True
                    ) as out_shm:
                        if out_shm is None:
                            raise RuntimeError(
                                "Could not allocate output shared memory."
                            )
                        serialized_result = out_shm.buf.tobytes()[1:]
                        status, result = cloudpickle.loads(serialized_result)

                        # send the termination signal to the subprocess.
                        out_shm.buf[0] = 1
                except RuntimeError:
                    # No output result in shm: This typically occurs when the subprocess
                    # early exits with exit code 0. e.g. exit(0)
                    status, result = "error", "No, output result found in shm."

                # wait for the subprocess to finish.
                proc.wait()

                stop_event.set()
                thread_stdout.join()
                thread_stderr.join()

                # print the stdout and stderr from subprocess.
                clear_subprocess_pipes(proc.stdout, proc.stderr)

                # close the pipes to subprocess
                proc.stdout.close()  # type: ignore
                proc.stdin.close()  # type: ignore
                proc.stderr.close()  # type: ignore

            if status == "error":
                raise Exception(f"Error in subprocess: {result}")

            return result

        return wrapper

    return run_subprocess
