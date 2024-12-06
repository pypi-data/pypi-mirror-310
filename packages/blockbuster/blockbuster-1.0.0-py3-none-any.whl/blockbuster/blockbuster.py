"""BlockBuster module."""

from __future__ import annotations

import asyncio
import inspect
import io
import os
import socket
import ssl
import sys
import time
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

import forbiddenfruit

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Iterator


class BlockingError(Exception):
    """BlockingError class."""


def _blocking_error(func: Callable[..., Any]) -> BlockingError:
    if inspect.isbuiltin(func):
        msg = f"Blocking call to {func.__qualname__} ({func.__self__})"
    elif inspect.ismethoddescriptor(func):
        msg = f"Blocking call to {func}"
    else:
        msg = f"Blocking call to {func.__module__}.{func.__qualname__}"
    return BlockingError(msg)


def wrap_blocking(
    func: Callable[..., Any],
    stack_excludes: list[tuple[str, Iterable[str]]],
    func_excludes: list[Callable[..., bool]],
) -> Callable[..., Any]:
    """Wrap blocking function."""

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return func(*args, **kwargs)
        for filename, functions in stack_excludes:
            for frame_info in inspect.stack():
                if (
                    frame_info.filename.endswith(filename)
                    and frame_info.function in functions
                ):
                    return func(*args, **kwargs)
        for func_exclude in func_excludes:
            if func_exclude(*args, **kwargs):
                return func(*args, **kwargs)
        raise _blocking_error(func)

    return wrapper


class BlockBusterFunction:
    """BlockBusterFunction class."""

    def __init__(
        self,
        module: Any,
        func_name: str,
        *,
        is_immutable: bool = False,
        stack_excludes: list[tuple[str, Iterable[str]]] | None = None,
        func_excludes: list[Callable[..., bool]] | None = None,
    ):
        """Initialize BlockBusterFunction."""
        self.module = module
        self.func_name = func_name
        self.original_func = getattr(module, func_name)
        self.is_immutable = is_immutable
        self.stack_excludes: list[tuple[str, Iterable[str]]] = stack_excludes or []
        self.func_excludes: list[Callable[..., bool]] = func_excludes or []

    def wrap_blocking(self) -> None:
        """Wrap the function."""
        checker = wrap_blocking(
            self.original_func, self.stack_excludes, self.func_excludes
        )
        if self.is_immutable:
            forbiddenfruit.curse(self.module, self.func_name, checker)
        else:
            setattr(self.module, self.func_name, checker)

    def unwrap_blocking(self) -> None:
        """Unwrap the function."""
        if self.is_immutable:
            forbiddenfruit.curse(self.module, self.func_name, self.original_func)
        else:
            setattr(self.module, self.func_name, self.original_func)


def _get_time_wrapped_functions() -> dict[str, BlockBusterFunction]:
    return {
        "time.sleep": BlockBusterFunction(
            time,
            "sleep",
            stack_excludes=[("pydev/pydevd.py", {"_do_wait_suspend"})],
        )
    }


def _get_os_wrapped_functions() -> dict[str, BlockBusterFunction]:
    def os_exclude(fd: int, *_: Any, **__: Any) -> bool:
        return not os.get_blocking(fd)

    return {
        "os.read": BlockBusterFunction(os, "read", func_excludes=[os_exclude]),
        "os.write": BlockBusterFunction(os, "write", func_excludes=[os_exclude]),
    }


def _get_io_wrapped_functions() -> dict[str, BlockBusterFunction]:
    def file_write_exclude(file: io.IOBase, *_: Any, **__: Any) -> bool:
        return file in {sys.stdout, sys.stderr}

    return {
        "io.BufferedReader.read": BlockBusterFunction(
            io.BufferedReader,
            "read",
            is_immutable=True,
            stack_excludes=[
                ("<frozen importlib._bootstrap_external>", {"get_data"}),
                ("_pytest/assertion/rewrite.py", {"_rewrite_test", "_read_pyc"}),
            ],
        ),
        "io.BufferedWriter.write": BlockBusterFunction(
            io.BufferedWriter,
            "write",
            is_immutable=True,
            stack_excludes=[("_pytest/assertion/rewrite.py", {"_write_pyc"})],
            func_excludes=[file_write_exclude],
        ),
        "io.BufferedRandom.read": BlockBusterFunction(
            io.BufferedRandom, "read", is_immutable=True
        ),
        "io.BufferedRandom.write": BlockBusterFunction(
            io.BufferedRandom,
            "write",
            is_immutable=True,
            func_excludes=[file_write_exclude],
        ),
        "io.TextIOWrapper.read": BlockBusterFunction(
            io.TextIOWrapper, "read", is_immutable=True
        ),
        "io.TextIOWrapper.write": BlockBusterFunction(
            io.TextIOWrapper,
            "write",
            is_immutable=True,
            func_excludes=[file_write_exclude],
        ),
    }


def _socket_exclude(sock: socket.socket, *_: Any, **__: Any) -> bool:
    return not sock.getblocking()


def _get_socket_wrapped_functions() -> dict[str, BlockBusterFunction]:
    return {
        f"socket.socket.{method}": BlockBusterFunction(
            socket.socket, method, func_excludes=[_socket_exclude]
        )
        for method in (
            "connect",
            "accept",
            "send",
            "sendall",
            "sendto",
            "recv",
            "recv_into",
            "recvfrom",
            "recvfrom_into",
            "recvmsg",
        )
    }


def _get_ssl_wrapped_functions() -> dict[str, BlockBusterFunction]:
    return {
        f"ssl.SSLSocket.{method}": BlockBusterFunction(
            ssl.SSLSocket, method, func_excludes=[_socket_exclude]
        )
        for method in ("write", "send", "read", "recv")
    }


class BlockBuster:
    """BlockBuster class."""

    def __init__(self) -> None:
        """Initialize BlockBuster."""
        self.wrapped_functions = (
            _get_time_wrapped_functions()
            | _get_os_wrapped_functions()
            | _get_io_wrapped_functions()
            | _get_socket_wrapped_functions()
            | _get_ssl_wrapped_functions()
        )

    def init(self) -> None:
        """Wrap all functions."""
        for wrapped_function in self.wrapped_functions.values():
            wrapped_function.wrap_blocking()

    def cleanup(self) -> None:
        """Unwrap all wrapped functions."""
        for wrapped_function in self.wrapped_functions.values():
            wrapped_function.unwrap_blocking()


@contextmanager
def blockbuster_ctx() -> Iterator[BlockBuster]:
    """Context manager for using BlockBuster."""
    blockbuster = BlockBuster()
    blockbuster.init()
    yield blockbuster
    blockbuster.cleanup()
