import unittest
import warnings

import k3ut
import k3handy

dd = k3ut.dd


class TestHandyCmd(unittest.TestCase):
    def test_parse_flag(self):
        # Test cases using deprecated single-letter flags
        # These still need to work but emit warnings
        deprecated_cases = [
            (["x"], ("raise",)),
            (["t"], ("tty",)),
            (["n"], ("none",)),
            (["p"], ("pass",)),
            (["o"], ("stdout",)),
            (["0"], ("oneline",)),
            (
                ["x0"],
                (
                    "raise",
                    "oneline",
                ),
            ),
            (["x0-x"], ("oneline",)),
            (
                ["x0-xx"],
                (
                    "oneline",
                    "raise",
                ),
            ),
            (
                ["x0", "-xx"],
                (
                    "oneline",
                    "raise",
                ),
            ),
            (
                ["x0", ""],
                (
                    "raise",
                    "oneline",
                ),
            ),
            (["x0", ["-oneline"]], ("raise",)),
        ]

        # Test cases using full flag names (no warnings expected)
        full_name_cases = [
            ([""], ()),
            ([("raise", "oneline", "-raise")], ("oneline",)),
            ([["raise", "oneline"]], ("raise", "oneline")),
        ]

        # Test deprecated single-letter flags (suppress expected warnings)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            for flags, want in deprecated_cases:
                got = k3handy.parse_flag(*flags)
                self.assertEqual(want, got)

            with self.assertRaises(KeyError):
                k3handy.parse_flag("q")

        # Test full name flags (no warnings)
        for flags, want in full_name_cases:
            got = k3handy.parse_flag(*flags)
            self.assertEqual(want, got)

    def test_parse_flag_with_enum(self):
        # Test CmdFlag enum
        got = k3handy.parse_flag(k3handy.CmdFlag.RAISE)
        self.assertEqual(("raise",), got)

        got = k3handy.parse_flag(k3handy.CmdFlag.RAISE, k3handy.CmdFlag.ONELINE)
        self.assertEqual(("raise", "oneline"), got)

        # Test list of enums
        got = k3handy.parse_flag([k3handy.CmdFlag.RAISE, k3handy.CmdFlag.STDOUT])
        self.assertEqual(("raise", "stdout"), got)

        # Test mixed string and enum
        got = k3handy.parse_flag(["raise", k3handy.CmdFlag.STDOUT])
        self.assertEqual(("raise", "stdout"), got)

        got = k3handy.parse_flag([k3handy.CmdFlag.RAISE, "stdout"])
        self.assertEqual(("raise", "stdout"), got)

    def test_enum_flags(self):
        # Test single enum flag
        got = k3handy.cmdf("python", "-c", 'print("a"); print("b")', flag=k3handy.CmdFlag.ONELINE)
        self.assertEqual("a", got)

        # Test list of enum flags
        got = k3handy.cmdf(
            "python",
            "-c",
            'print("a"); print("b")',
            flag=[k3handy.CmdFlag.RAISE, k3handy.CmdFlag.STDOUT],
        )
        self.assertEqual(["a", "b"], got)

        # Test enum flag with error handling
        self.assertRaises(
            k3handy.CalledProcessError,
            k3handy.cmdf,
            "python",
            "-c",
            "import sys; sys.exit(5)",
            flag=[k3handy.CmdFlag.RAISE, k3handy.CmdFlag.ONELINE],
        )

        # Test NONE enum flag
        got = k3handy.cmdf(
            "python",
            "-c",
            "import sys; sys.exit(5)",
            flag=[k3handy.CmdFlag.NONE, k3handy.CmdFlag.ONELINE],
        )
        self.assertEqual(None, got)

    def test_preset_combinations(self):
        # Test CMD_RAISE_ONELINE
        got = k3handy.cmdf("python", "-c", 'print("a"); print("b")', flag=k3handy.CMD_RAISE_ONELINE)
        self.assertEqual("a", got)

        # Test CMD_RAISE_STDOUT
        got = k3handy.cmdf(
            "python",
            "-c",
            'print("a"); print("b")',
            flag=k3handy.CMD_RAISE_STDOUT,
        )
        self.assertEqual(["a", "b"], got)

        # Test CMD_NONE_ONELINE with error
        got = k3handy.cmdf(
            "python",
            "-c",
            "import sys; sys.exit(5)",
            flag=k3handy.CMD_NONE_ONELINE,
        )
        self.assertEqual(None, got)

        # Test CMD_RAISE_STDOUT with error
        self.assertRaises(
            k3handy.CalledProcessError,
            k3handy.cmdf,
            "python",
            "-c",
            "import sys; sys.exit(5)",
            flag=k3handy.CMD_RAISE_STDOUT,
        )

    def test_mixed_string_enum_usage(self):
        # Mix string and enum in list
        got = k3handy.cmdf(
            "python",
            "-c",
            'print("a"); print("b")',
            flag=["raise", k3handy.CmdFlag.STDOUT],
        )
        self.assertEqual(["a", "b"], got)

        got = k3handy.cmdf(
            "python",
            "-c",
            'print("a"); print("b")',
            flag=[k3handy.CmdFlag.RAISE, "stdout"],
        )
        self.assertEqual(["a", "b"], got)

    def test_cmdf(self):
        got = k3handy.cmdf("python", "-c", 'print("a"); print("b")', flag=["oneline"])
        self.assertEqual("a", got)

        #  no output
        got = k3handy.cmdf("python", "-c", "", flag=["oneline"])
        self.assertEqual("", got)

        # not raise without 'raise'
        k3handy.cmdf(
            "python",
            "-c",
            "import sys; sys.exit(5)",
            flag=["oneline"],
        )

        # return None if error
        got = k3handy.cmdf(
            "python",
            "-c",
            "import sys; sys.exit(5)",
            flag=["none", "oneline"],
        )
        self.assertEqual(None, got)

        #  raise with 'raise'
        self.assertRaises(
            k3handy.CalledProcessError,
            k3handy.cmdf,
            "python",
            "-c",
            "import sys; sys.exit(5)",
            flag=["raise", "oneline"],
        )

        self.assertRaises(
            k3handy.CalledProcessError,
            k3handy.cmdx,
            "python",
            "-c",
            "import sys; sys.exit(5)",
        )

        # stdout
        got = k3handy.cmdf(
            "python",
            "-c",
            'print("a"); print("b")',
            flag=["stdout"],
        )
        self.assertEqual(["a", "b"], got)

        self.assertRaises(
            k3handy.CalledProcessError,
            k3handy.cmdf,
            "python",
            "-c",
            "import sys; sys.exit(5)",
            flag=["raise", "stdout"],
        )

        # tty
        returncode, out, err = k3handy.cmdf(
            "python",
            "-c",
            "import sys; print(sys.stdout.isatty())",
            flag=["tty"],
        )

        dd("out:", out)
        self.assertEqual(["True"], out)

        returncode, out, err = k3handy.cmdtty(
            "python",
            "-c",
            "import sys; print(sys.stdout.isatty())",
        )
        dd("out:", out)
        self.assertEqual(["True"], out)

        # input
        read_stdin_in_subproc = """
import k3handy;
k3handy.cmdf(
'python', '-c', 'import sys; print(sys.stdin.read())',
flag=['pass']
)
        """

        returncode, out, err = k3handy.cmdx(
            "python",
            "-c",
            read_stdin_in_subproc,
            input="123",
        )

        dd("out:", out)
        self.assertEqual(["123"], out)

    def test_cmd0(self):
        got = k3handy.cmd0(
            "python",
            "-c",
            'print("a"); print("b")',
        )
        self.assertEqual("a", got)

        #  no output

        got = k3handy.cmd0(
            "python",
            "-c",
            "",
        )
        self.assertEqual("", got)

        #  failure to exception

        self.assertRaises(
            k3handy.CalledProcessError,
            k3handy.cmd0,
            "python",
            "-c",
            "import sys; sys.exit(5)",
        )

    def test_cmdout(self):
        got = k3handy.cmdout(
            "python",
            "-c",
            'print("a"); print("b")',
        )
        self.assertEqual(["a", "b"], got)

        self.assertRaises(
            k3handy.CalledProcessError,
            k3handy.cmdout,
            "python",
            "-c",
            "import sys; sys.exit(5)",
        )

    def test_cmdx(self):
        got = k3handy.cmdx(
            "python",
            "-c",
            'print("a"); print("b")',
        )
        self.assertEqual((0, ["a", "b"], []), got)

        self.assertRaises(
            k3handy.CalledProcessError,
            k3handy.cmdx,
            "python",
            "-c",
            "import sys; sys.exit(5)",
        )

    def test_cmdtty(self):
        returncode, out, err = k3handy.cmdtty(
            "python",
            "-c",
            "import sys; print(sys.stdout.isatty())",
        )

        dd("returncode:", returncode)
        dd("out:", out)
        dd("err:", err)

        self.assertEqual(0, returncode)
        self.assertEqual(["True"], out)
        self.assertEqual([], err)

    def test_cmdpass(self):
        read_stdin_in_subproc = """
import k3handy;
k3handy.cmdpass(
'python', '-c', 'import sys; print(sys.stdin.read())',
)
        """

        returncode, out, err = k3handy.cmdx(
            "python",
            "-c",
            read_stdin_in_subproc,
            input="123",
        )

        dd("returncode:", returncode)
        dd("out:", out)
        dd("err:", err)

        self.assertEqual(0, returncode)
        self.assertEqual(["123"], out)
