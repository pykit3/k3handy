"""
k3handy is collection of mostly used  utilities.
"""

from __future__ import annotations

import logging
import os
from collections.abc import Sequence

from k3fs import fread, fwrite, ls_dirs, ls_files, makedirs, remove
from k3proc import CalledProcessError, TimeoutExpired, command
from k3str import to_bytes

from . import path
from .cmdutil import (
    CMD_NONE_ONELINE,
    CMD_RAISE_ONELINE,
    CMD_RAISE_STDOUT,
    CmdFlag,
    cmd0,
    cmdf,
    cmdout,
    cmdpass,
    cmdtty,
    cmdx,
    dd,
    ddstack,
    parse_flag,
)
from .path import pabs, pjoin, prebase

# Grouped by source module, not sorted.
__all__ = [  # noqa: RUF022
    # from k3fs
    "fread",
    "fwrite",
    "ls_dirs",
    "ls_files",
    "makedirs",
    "remove",
    # from k3proc
    "command",
    "CalledProcessError",
    "TimeoutExpired",
    # from k3str
    "to_bytes",
    # from .path
    "path",
    "pabs",
    "pjoin",
    "prebase",
    # from .cmd
    "CmdFlag",
    "CMD_RAISE_STDOUT",
    "CMD_RAISE_ONELINE",
    "CMD_NONE_ONELINE",
    "cmd0",
    "cmdf",
    "cmdout",
    "cmdpass",
    "cmdtty",
    "cmdx",
    "parse_flag",
    "dd",
    "ddstack",
    # local
    "display",
]

logger = logging.getLogger(__name__)

#  Since 3.8 there is a stacklevel argument
ddstack_kwarg: dict[str, int] = {"stacklevel": 2}


def display(
    stdout: int | str | Sequence[str] | None,
    stderr: str | Sequence[str] | None = None,
) -> None:
    """
    Output to stdout and stderr.
    - ``display(1, "foo")`` write to stdout.
    - ``display(1, ["foo", "bar"])`` write multilines to stdout.
    - ``display(1, ("foo", "bar"))`` write multilines to stdout.
    - ``display(("foo", "bar"), ["woo"])`` write multilines to stdout and stderr.
    - ``display(None, ["woo"])`` write multilines to stderr.

    """

    if isinstance(stdout, int):
        fd = stdout
        line = stderr

        if isinstance(line, (list, tuple)):
            lines = line
            for ln in lines:
                display(fd, ln)
            return

        os.write(fd, to_bytes(line))
        os.write(fd, b"\n")
        return

    if stdout is not None:
        display(1, stdout)

    if stderr is not None:
        display(2, stderr)


def __getattr__(name: str) -> str:
    # importlib.metadata takes about 20 ms to import, so it is loaded only
    # when __version__ is read
    if name != "__version__":
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    from importlib.metadata import version

    return version("k3handy")
