from __future__ import annotations

import inspect
import logging
import sys
import warnings
from enum import Enum
from typing import Any, Sequence, Union

from k3proc import command

logger = logging.getLogger(__name__)


class CmdFlag(str, Enum):
    """Command execution flags for cmdf() and related functions.

    Flags control subprocess behavior and return value formatting.
    Can be used individually or combined in lists.

    Examples:
        >>> cmdf("ls", flag=CmdFlag.RAISE)
        >>> cmdf("git", "status", flag=[CmdFlag.RAISE, CmdFlag.STDOUT])
        >>> cmdf("echo", "hi", flag=CMD_RAISE_ONELINE)
    """

    RAISE = "raise"  # Raise CalledProcessError if return code != 0
    TTY = "tty"  # Start subprocess in a tty
    NONE = "none"  # Return None if return code != 0
    PASS = "pass"  # Don't capture stdin/stdout/stderr
    STDOUT = "stdout"  # Return stdout as list[str]
    ONELINE = "oneline"  # Return first line of stdout


# Preset combinations for common usage patterns
CMD_RAISE_STDOUT: list[str] = [CmdFlag.RAISE, CmdFlag.STDOUT]
CMD_RAISE_ONELINE: list[str] = [CmdFlag.RAISE, CmdFlag.ONELINE]
CMD_NONE_ONELINE: list[str] = [CmdFlag.NONE, CmdFlag.ONELINE]

# Type alias for flag parameters  (using Union for Python 3.9 compatibility)
CmdFlagType = Union[str, CmdFlag, Sequence[Union[str, CmdFlag]]]

#  Since 3.8 there is a stacklevel argument
ddstack_kwarg: dict[str, Any] = {}
if sys.version_info.major == 3 and sys.version_info.minor >= 8:
    ddstack_kwarg = {"stacklevel": 2}


def dd(*msg: Any) -> None:
    """
    Alias to logger.debug()
    """
    msg_strs = [str(x) for x in msg]
    msg_str = " ".join(msg_strs)
    logger.debug(msg_str, **ddstack_kwarg)


def ddstack(*msg: Any) -> None:
    """
    Log calling stack in logging.DEBUG level.
    """

    if logger.isEnabledFor(logging.DEBUG):
        stack = inspect.stack()[1:]
        for i, (frame, path, ln, func, lines, xx) in enumerate(stack):
            #  python -c "xxx" does not have a line
            if lines is None:
                line_str = ""
            else:
                line_str = lines[0].strip()
            logger.debug("stack: %d %s %s", ln, func, line_str, **ddstack_kwarg)


def cmdf(
    cmd: str | Sequence[str],
    *arguments: str,
    flag: CmdFlagType = "",
    **options: Any,
) -> None | list[str] | str | tuple[int, list[str], list[str]]:
    """
    Alias to k3proc.command(). Behavior is specified with ``flag``

    Args:
        cmd: the path to executable

        arguments: command arguments

        flag: Execution flags (use CmdFlag enum recommended, strings also supported)

            Individual flags (use CmdFlag enum):
                - CmdFlag.RAISE: raise CalledProcessError if return code != 0
                - CmdFlag.TTY: start subprocess in a tty
                - CmdFlag.NONE: return None if return code != 0
                - CmdFlag.PASS: don't capture stdin/stdout/stderr
                - CmdFlag.STDOUT: return stdout as list[str]
                - CmdFlag.ONELINE: return first line of stdout

            Preset combinations:
                - CMD_RAISE_STDOUT: [CmdFlag.RAISE, CmdFlag.STDOUT]
                - CMD_RAISE_ONELINE: [CmdFlag.RAISE, CmdFlag.ONELINE]
                - CMD_NONE_ONELINE: [CmdFlag.NONE, CmdFlag.ONELINE]

            String forms also supported: 'raise', 'tty', 'none', 'pass', 'stdout', 'oneline'

            .. deprecated::
                Single-letter flags are deprecated, use CmdFlag enum or full names instead:
                    - 'x' or ('raise',): raise CalledProcessError if return code != 0
                    - 't' or ('tty',): start subprocess in a tty
                    - 'n' or ('none',): return None if return code != 0
                    - 'p' or ('pass',): don't capture stdin/stdout/stderr
                    - 'o' or ('stdout',): return stdout as list[str]
                    - '0' or ('oneline',): return first line of stdout

        options: other options passed to k3proc.command()

    Returns:
        Varies based on flags:
            - With ONELINE: str (first line of stdout)
            - With STDOUT: list[str] (all stdout lines)
            - With NONE: None if error, otherwise normal return
            - Default: tuple[int, list[str], list[str]] (code, stdout, stderr)

    Examples:
        Using enum constants (recommended):

        >>> cmdf("ls", "-la", flag=CmdFlag.RAISE)
        >>> cmdf("git", "status", flag=[CmdFlag.RAISE, CmdFlag.STDOUT])
        >>> branch = cmdf("git", "branch", "--show-current", flag=CMD_RAISE_ONELINE)

        String forms (also supported):

        >>> cmdf("ls", flag="raise")
        >>> cmdf("ls", flag=["raise", "stdout"])
    """
    dd("cmdf:", cmd, arguments, options)
    dd("flag:", flag)
    flag = parse_flag(flag)

    if "raise" in flag:
        options["check"] = True
    if "tty" in flag:
        options["tty"] = True
    if "pass" in flag:
        options["capture"] = False

    code, out, err = command(cmd, *arguments, **options)

    # reaching here means there is no check of exception
    if code != 0 and "none" in flag:
        return None

    out_lines = out.splitlines() if isinstance(out, str) else out.decode().splitlines()
    err_lines = err.splitlines() if isinstance(err, str) else err.decode().splitlines()

    if "stdout" in flag:
        dd("cmdf: out:", out_lines)
        return out_lines

    if "oneline" in flag:
        dd("cmdf: out:", out_lines)
        if len(out_lines) > 0:
            return out_lines[0]
        return ""

    return code, out_lines, err_lines


def cmd0(cmd: str | Sequence[str], *arguments: str, **options: Any) -> str:
    """
    Alias to k3proc.command() with ``check=True``

    Returns:
        str: first line of stdout.
    """
    dd("cmd0:", cmd, arguments, options)
    _, out, _ = cmdx(cmd, *arguments, **options)
    dd("cmd0: out:", out)
    if len(out) > 0:
        return out[0]
    return ""


def cmdout(cmd: str | Sequence[str], *arguments: str, **options: Any) -> list[str]:
    """
    Alias to k3proc.command() with ``check=True``.

    Returns:
        list: stdout in lines of str.
    """

    dd("cmdout:", cmd, arguments, options)
    _, out, _ = cmdx(cmd, *arguments, **options)
    dd("cmdout: out:", out)
    return out


def cmdx(cmd: str | Sequence[str], *arguments: str, **options: Any) -> tuple[int, list[str], list[str]]:
    """
    Alias to k3proc.command() with ``check=True``.

    Returns:
        (int, list, list): exit code, stdout and stderr in lines of str.
    """
    dd("cmdx:", cmd, arguments, options)
    ddstack()

    options["check"] = True
    code, out, err = command(cmd, *arguments, **options)
    out_lines = out.splitlines() if isinstance(out, str) else out.decode().splitlines()
    err_lines = err.splitlines() if isinstance(err, str) else err.decode().splitlines()
    return code, out_lines, err_lines


def cmdtty(cmd: str | Sequence[str], *arguments: str, **options: Any) -> tuple[int, list[str], list[str]]:
    """
    Alias to k3proc.command() with ``check=True`` ``tty=True``.
    As if the command is run in a tty.

    Returns:
        (int, list, list): exit code, stdout and stderr in lines of str.
    """

    dd("cmdtty:", cmd, arguments, options)
    options["tty"] = True
    return cmdx(cmd, *arguments, **options)


def cmdpass(cmd: str | Sequence[str], *arguments: str, **options: Any) -> tuple[int, list[str], list[str]]:
    """
    Alias to k3proc.command() with ``check=True`` ``capture=False``.
    It just passes stdout and stderr to calling process.

    Returns:
        (int, list, list): exit code and empty stdout and stderr.
    """
    # interactive mode, delegate stdin to sub proc
    dd("cmdpass:", cmd, arguments, options)
    options["capture"] = False
    return cmdx(cmd, *arguments, **options)


def parse_flag(*flags: str | CmdFlag | Sequence[str | CmdFlag]) -> tuple[str, ...]:
    """
    Convert short form flag into tuple form, e.g.:
    parse_flag('x0') output: ('raise', 'oneline')

    '-x' will remove flag 'x'.
    parse_flag('x0-x') output ('online', )

    parse_flag(['raise', 'oneline', '-raise']) outputs ('oneline', )

    parse_flag(['raise', 'oneline', '-raise'], 't') outputs ('oneline', 'tty', )

    .. deprecated::
        Single-letter flags ('x', 't', 'n', 'p', 'o', '0') are deprecated.
        Use full names ('raise', 'tty', 'none', 'pass', 'stdout', 'oneline') instead.

    """

    expanded: list[str] = []
    for flag in flags:
        f = expand_flag(flag)
        expanded.extend(f)

    #  reduce

    res: dict[str, bool] = {}
    for key in expanded:
        if key.startswith("-"):
            key = key[1:]
            if key in res:
                del res[key]
        else:
            res[key] = True

    result = tuple(res.keys())

    return result


def expand_flag(flag: str | CmdFlag | Sequence[str | CmdFlag]) -> tuple[str, ...] | Sequence[str]:
    # expand abbreviations:
    # x  ->  raise
    # -x -> -raise

    # Handle CmdFlag enum
    if isinstance(flag, CmdFlag):
        return (flag.value,)

    mp: dict[str, str] = {
        "x": "raise",
        "t": "tty",
        "n": "none",
        "p": "pass",
        "o": "stdout",
        "0": "oneline",
    }

    if isinstance(flag, str):
        res: list[str] = []
        buf = ""

        for c in flag:
            if c == "-":
                buf += c
                continue
            else:
                full_name = mp[c]
                warnings.warn(
                    f"Single-letter flag '{c}' is deprecated, use '{full_name}' instead",
                    DeprecationWarning,
                    stacklevel=4,
                )
                key = buf + full_name
                buf = ""

                res.append(key)

        return tuple(res)
    return flag
