import os
import unittest

import k3ut
import k3handy

dd = k3ut.dd

this_base = os.path.dirname(__file__)


class TestHandyLogging(unittest.TestCase):

    foo_fn = '/tmp/foo'

    def _clean(self):

        # remove written file
        try:
            os.unlink(self.foo_fn)
        except EnvironmentError:
            pass

    def setUp(self):
        self._clean()

    def tearDown(self):
        self._clean()

class TestHandyCmd(unittest.TestCase):

    foo_fn = '/tmp/foo'

    def _clean(self):

        # remove written file
        try:
            os.unlink(self.foo_fn)
        except EnvironmentError:
            pass

    def setUp(self):
        self._clean()

    def tearDown(self):
        self._clean()

    def test_cmd0(self):
        got = k3handy.cmd0(
            'python', '-c', 'print("a"); print("b")',
        )
        self.assertEqual('a', got)

        self.assertRaises(k3handy.CalledProcessError,
                          k3handy.cmd0,
                          'python', '-c',
                          'import sys; sys.exit(5)',
                          )

    def test_cmdout(self):
        got = k3handy.cmdout(
            'python', '-c', 'print("a"); print("b")',
        )
        self.assertEqual(['a', 'b'], got)

        self.assertRaises(k3handy.CalledProcessError,
                          k3handy.cmdout,
                          'python', '-c',
                          'import sys; sys.exit(5)',
                          )
    def test_cmdx(self):
        got = k3handy.cmdx(
            'python', '-c', 'print("a"); print("b")',
        )
        self.assertEqual((0, ['a', 'b'], []), got)

        self.assertRaises(k3handy.CalledProcessError,
                          k3handy.cmdx,
                          'python', '-c',
                          'import sys; sys.exit(5)',
                          )

    def test_cmdtty(self):
        returncode, out, err = k3handy.cmdtty(
            'python', '-c', 'import sys; print(sys.stdout.isatty())',
            tty=True,
        )

        dd('returncode:', returncode)
        dd('out:', out)
        dd('err:', err)

        self.assertEqual(0, returncode)
        self.assertEqual(['True'], out)
        self.assertEqual([], err)

    def test_cmdpass(self):
        read_stdin_in_subproc = '''
import k3handy;
k3handy.cmdpass(
'python', '-c', 'import sys; print(sys.stdin.read())',
)
        '''

        returncode, out, err = k3handy.cmdx(
            'python', '-c',
            read_stdin_in_subproc,
            input="123",
        )

        dd('returncode:', returncode)
        dd('out:', out)
        dd('err:', err)

        self.assertEqual(0, returncode)
        self.assertEqual(["123"], out)
