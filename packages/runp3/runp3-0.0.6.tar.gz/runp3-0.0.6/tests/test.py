#!/usr/bin/env python
"""runp test scripts."""

import io
import sys
import unittest
from pathlib import Path

from runp import runp


class RunPTestCase(unittest.TestCase):
    """runp3 test class."""

    def setUp(self) -> None:
        """setup."""
        self.test_path = Path(__file__).parent
        self.runfile = self.test_path.joinpath("testfile.py")
        self.imported_vars = runp.load_runfile(self.runfile)
        self.functions = runp.filter_vars(self.imported_vars)
        self.org_stdout, sys.stdout = sys.stdout, io.StringIO()
        self.org_stderr, sys.stderr = sys.stderr, io.StringIO()

    def tearDown(self) -> None:
        """teardown."""
        sys.stdout = self.org_stdout
        sys.stderr = self.org_stderr

    def test_load_runfile(self) -> None:
        """Run the test of load testfile."""
        self.assertTrue(len(self.imported_vars) >= len(self.functions))

    def test_filter_vars(self) -> None:
        """Run the test of load testfile."""
        self.assertEqual(len(self.functions), 4)

    def test_print_functions(self) -> None:
        """Run the test of print_functions()."""
        out = """Available functions:
Wip.print_it\t
wet\t
wat\tWEEE
wut\tSuper docstring test"""
        runp.print_functions(self.functions)
        output = sys.stdout.getvalue().strip()  # type: ignore
        self.assertEqual(str(output), out)

    def test_print_function_no_docstring(self) -> None:
        """Run the test of print_function() without docstring."""
        out = """Displaying docstring for function wet in module testfile

wet() -> None"""
        runp.print_function(self.functions, "wet")
        output = sys.stdout.getvalue().strip()  # type: ignore
        self.assertEqual(str(output), out)

    def test_print_function_multi_docstring(self) -> None:
        """Run the test of print_function() with docstring."""
        out = """Displaying docstring for function wut in module testfile

wut(text: str, woop: bool = False) -> None
    Super docstring test
    
    Args:
        text (str): The text to print
        woop (boolean, optional): Default false"""
        runp.print_function(self.functions, "wut")
        output = sys.stdout.getvalue().strip()  # type: ignore
        self.assertEqual(str(output), out)

    def test_run_function_noargs(self) -> None:
        """Run the test of run_function() no args."""
        out = "testing, 1, 2, 3"
        runp.run_function(self.functions, "wat")
        output = sys.stdout.getvalue().strip()  # type: ignore
        self.assertEqual(str(output), out)

    def test_run_function_args(self) -> None:
        """Run the test of run_function() with args."""
        out = "mytext\ndoobey"
        runp.run_function(self.functions, "wut:mytext,doobey")
        output = sys.stdout.getvalue().strip()  # type: ignore
        self.assertEqual(str(output), out)

    def test_run_function_named_args(self) -> None:
        """Run the test of run_function() with named args."""
        out = "mytext\nTrue"
        runp.run_function(self.functions, "wut:mytext,woop=True")
        output = sys.stdout.getvalue().strip()  # type: ignore
        self.assertEqual(str(output), out)

    def test_run_function_reverse_args(self) -> None:
        """Run the test of run_function() with reverse args."""
        out = "mytext\nTrue"
        runp.run_function(self.functions, "wut:woop=True,mytext")
        output = sys.stdout.getvalue().strip()  # type: ignore
        self.assertEqual(str(output), out)

    def test_run_function_wrong_args(self) -> None:
        """Run the test of run_function() with wrong args."""
        out = "wut() missing 1 required positional argument: 'text'"
        runp.run_function(self.functions, "wut")
        output = sys.stdout.getvalue().strip()  # type: ignore
        self.assertEqual(str(output), out)

    def test_get_function_nonexistant(self) -> None:
        """Run the test of get_function() no exists."""
        nofunc = "wutwut"
        out = "No function named '{}' found!".format(nofunc)
        runp.get_function(self.functions, nofunc)
        output = sys.stdout.getvalue().strip()  # type: ignore
        self.assertEqual(str(output), out)

    def test_parse_args_noargs(self) -> None:
        """Run the test of parse_args() no args."""
        inputstr = "wut"
        cmd, args, kwargs = runp.parse_args(inputstr)
        tup = (cmd, args, kwargs)
        self.assertEqual(tup, ("wut", [], {}))

    def test_parse_args_nokwargs(self) -> None:
        """Run the test of parse_args() no kwargs."""
        inputstr = "wut:wow,such,good"
        cmd, args, kwargs = runp.parse_args(inputstr)
        tup = (cmd, args, kwargs)
        self.assertEqual(tup, ("wut", ["wow", "such", "good"], {}))

    def test_parse_args(self) -> None:
        """Run the test of parse_args() with args."""
        inputstr = "wut:arg=wow,'such spaces',arg2=good"
        cmd, args, kwargs = runp.parse_args(inputstr)
        tup = (cmd, args, kwargs)
        self.assertEqual(
            tup,
            ("wut", ["'such spaces'"], {"arg": "wow", "arg2": "good"})
        )

    def test_escape_split_comma(self) -> None:
        """Run the test of _escape_split() split comma."""
        inputstr = "wut:arg=wow,'such spaces',arg2=good"
        splitted = ['wut:arg=wow', "'such spaces'", 'arg2=good']
        self.assertEqual(runp._escape_split(',', inputstr), splitted)

    def test_escape_split_equals(self) -> None:
        """Run the test of _escape_split() split equals."""
        inputstrs = ['wut:arg=wow', "'such spaces'", 'arg2=good']
        results = [['wut:arg', 'wow'], ["'such spaces'"], ['arg2', 'good']]
        for i, inputstr in enumerate(inputstrs):
            self.assertEqual(runp._escape_split('=', inputstr), results[i])

    def test_escape_split_escape_comma(self) -> None:
        """Run the test of _escape_split() escape comma."""
        inputstr = "wut:arg=wow\\,,'such spaces',arg2=good"
        splitted = ['wut:arg=wow,', "'such spaces'", 'arg2=good']
        self.assertEqual(runp._escape_split(',', inputstr), splitted)

    def test_escape_split_escape_equals(self) -> None:
        """Run the test of _escape_split() escape equals."""
        inputstrs = ['wut:arg=wow\\=', "'such spaces'", 'arg2=good']
        results = [['wut:arg', 'wow='], ["'such spaces'"], ['arg2', 'good']]
        for i, inputstr in enumerate(inputstrs):
            self.assertEqual(runp._escape_split('=', inputstr), results[i])

    def test_args_none(self) -> None:
        """Run the test of main() None"""
        with self.assertRaises(SystemExit):
            runp.main()

        output: str = sys.stdout.getvalue().strip()  # type: ignore
        error: str = sys.stderr.getvalue().strip()  # type: ignore
        self.assertEqual(output, "")
        self.assertTrue(error.startswith("usage: runp"))

    def test_args_empty(self) -> None:
        """Run the test of main() empty."""
        with self.assertRaises(SystemExit):
            runp.main(list())

        output: str = sys.stdout.getvalue().strip()  # type: ignore
        error: str = sys.stderr.getvalue().strip()  # type: ignore
        self.assertEqual(output, "")
        self.assertTrue(error.startswith("usage: runp"))

    def test_args_is_not_file(self) -> None:
        """Run the test of main() not file."""
        with self.assertRaises(SystemExit):
            runp.main([".\\tests"])

        output: str = sys.stdout.getvalue().strip()  # type: ignore
        error: str = sys.stderr.getvalue().strip()  # type: ignore
        self.assertEqual(output, "No such file '.\\tests'")
        self.assertEqual(error, "")

    def test_args_is_invalid(self) -> None:
        """Run the test of main() invalid."""
        with self.assertRaises(SystemExit):
            runp.main([".\\invalid"])

        output: str = sys.stdout.getvalue().strip()  # type: ignore
        error: str = sys.stderr.getvalue().strip()  # type: ignore
        self.assertEqual(output, "No such file '.\\invalid'")
        self.assertEqual(error, "")

    def test_args_file_only(self) -> None:
        """Run the test of main() file only."""
        with self.assertRaises(SystemExit):
            runp.main(["./tests/testfile.py"])

        output: str = sys.stdout.getvalue().strip()  # type: ignore
        error: str = sys.stderr.getvalue().strip()  # type: ignore
        self.assertEqual(output, "No function was selected!")
        self.assertEqual(error, "")

    def test_args_list_short(self) -> None:
        """Run the test of main() list(-l)."""
        out = """Available functions:
Wip.print_it\t
wet\t
wat\tWEEE
wut\tSuper docstring test"""

        with self.assertRaises(SystemExit):
            runp.main(["./tests/testfile.py", "-l"])

        output: str = sys.stdout.getvalue().strip()  # type: ignore
        error: str = sys.stderr.getvalue().strip()  # type: ignore
        self.assertEqual(output, out)
        self.assertEqual(error, "")

    def test_args_list_long(self) -> None:
        """Run the test of main() list(--list)."""
        out = """Available functions:
Wip.print_it\t
wet\t
wat\tWEEE
wut\tSuper docstring test"""

        with self.assertRaises(SystemExit):
            runp.main(["./tests/testfile.py", "--list"])

        output: str = sys.stdout.getvalue().strip()  # type: ignore
        error: str = sys.stderr.getvalue().strip()  # type: ignore
        self.assertEqual(output, out)
        self.assertEqual(error, "")

    def test_args_details_short(self) -> None:
        """Run the test of main() details(-d)."""
        out = """Displaying docstring for function wut in module testfile

wut(text: str, woop: bool = False) -> None
    Super docstring test
    
    Args:
        text (str): The text to print
        woop (boolean, optional): Default false"""

        with self.assertRaises(SystemExit):
            runp.main(["./tests/testfile.py", "-d", "wut"])

        output: str = sys.stdout.getvalue().strip()  # type: ignore
        error: str = sys.stderr.getvalue().strip()  # type: ignore
        self.assertEqual(output, out)
        self.assertEqual(error, "")

    def test_args_details_long(self) -> None:
        """Run the test of main() details(-details)."""
        out = """Displaying docstring for function wut in module testfile

wut(text: str, woop: bool = False) -> None
    Super docstring test
    
    Args:
        text (str): The text to print
        woop (boolean, optional): Default false"""

        with self.assertRaises(SystemExit):
            runp.main(["./tests/testfile.py", "--detail", "wut"])

        output: str = sys.stdout.getvalue().strip()  # type: ignore
        error: str = sys.stderr.getvalue().strip()  # type: ignore
        self.assertEqual(output, out)
        self.assertEqual(error, "")

    def test_args_list(self) -> None:
        """Run the test of main() list."""
        out = """testing, 1, 2, 3"""

        runp.main(["./tests/testfile.py", "wat"])

        output: str = sys.stdout.getvalue().strip()  # type: ignore
        error: str = sys.stderr.getvalue().strip()  # type: ignore
        self.assertEqual(output, out)
        self.assertEqual(error, "")


if __name__ == '__main__':
    unittest.main()
