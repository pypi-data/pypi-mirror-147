#!/usr/bin/env python
"""runp.

This repository is a modified of runp, which is no longer maintained, for modern Python 3.

runp exports Python functions from files to the command line.
You don't need to change your existing code.
"""

import sys
import argparse
import inspect
import pydoc
from typing import Dict, List, Tuple, Callable, Optional
from pathlib import Path
from types import ModuleType
from collections.abc import ItemsView


def filter_vars(imported_vars: ItemsView) -> Dict[str, Callable]:
    """Gets the name and object of the callable object from the imported_vars.

    Args:
        imported_vars (ItemsView): python module items iterator.

    Returns:
        Dict[str, Callable]: dictionary of name and callable object
    """
    functions = {}
    for name, obj in imported_vars:
        if callable(obj) and not name.startswith('_'):
            if inspect.isclass(obj):
                methods = inspect.getmembers(obj(), predicate=inspect.ismethod)
                for name, method in methods:
                    if not name.startswith('_'):
                        functions[obj.__name__ + "." + name] = method
            else:
                functions[obj.__name__] = obj
    return functions


def load_runfile(runfile: Path) -> ItemsView:
    """Load Python file.

    Args:
        runfile (Path): Python file path.

    Returns:
        ItemsView: python module items iterator.
    """
    importer = __import__
    directory, runfile = runfile.parent, Path(runfile.name)

    sys.path.insert(0, str(directory))
    imported: ModuleType = importer(runfile.stem)
    del sys.path[0]
    imported_vars = vars(imported).items()
    return imported_vars


def _escape_split(sep: str, argstr: str) -> List[str]:
    """Split function with escape characters.

    Args:
        sep (str): Split character.
        argstr (str): String to be divided.

    Returns:
        List[str]: List of splited strings.
    """
    escaped_sep = r'\%s' % sep

    if escaped_sep not in argstr:
        return argstr.split(sep)

    before, _, after = argstr.partition(escaped_sep)
    startlist = before.split(sep)
    unfinished = startlist[-1]
    startlist = startlist[:-1]
    endlist = _escape_split(sep, after)
    unfinished += sep + endlist[0]
    return startlist + [unfinished] + endlist[1:]


def parse_args(cmd: str) -> Tuple[str, List[str], Dict[str, str]]:
    """Argment parser.

    Args:
        cmd (str): argment.

    Returns:
        Tuple[str, List[str], Dict[str, str]]: original argument,
        positional argument, and key word argument.
    """
    args = []
    kwargs = {}
    if ':' in cmd:
        cmd, argstr = cmd.split(':', 1)
        for pair in _escape_split(',', argstr):
            result = _escape_split('=', pair)
            if len(result) > 1:
                k, v = result
                kwargs[k] = v
            else:
                args.append(result[0])
    return cmd, args, kwargs


def get_docstring(function: Callable, abbrv: bool = False) -> str:
    """Get docstring.

    Args:
        function (Callable): targe callable object
        abbrv (bool, optional): Defaults to False.

    Returns:
        str: docstring.
    """
    doc = inspect.getdoc(function)
    if abbrv and doc is not None:
        doc = doc.splitlines()[0].strip()
    else:
        doc = ""
    return doc


def get_function(functions: Dict[str, Callable], function_name: str) -> Optional[Callable]:
    """Get function.

    Args:
        functions (Dict[str, Callable]): original function dictionaly.
        function_name (str): search function name.

    Returns:
        Optional[Callable]: find callable object.
    """
    try:
        return functions[function_name]
    except KeyError:
        print("No function named '{}' found!".format(function_name))
        return None


def print_functions(functions: Dict[str, Callable]) -> None:
    """Print functions list.

    Args:
        functions (Dict[str, Callable]): Print functions
    """
    print("Available functions:")
    for fname, function in functions.items():
        doc = get_docstring(function, abbrv=True)
        print(fname + "\t" + doc if doc is not None else "")


def print_function(functions: Dict[str, Callable], function: str) -> None:
    """Print function.

    Args:
        functions (Dict[str, Callable]): Print functions.
        function (str): function name.
    """
    func = get_function(functions, function)
    if func:
        print(pydoc.plain(pydoc.render_doc(
            func,
            "Displaying docstring for %s")
        ))


def run_function(functions: Dict[str, Callable], cmd: str) -> None:
    """Run function.

    Args:
        functions (Dict[str, Callable]): Print functions.
        cmd (str): command.
    """
    function, args, kwargs = parse_args(cmd)
    try:
        func = get_function(functions, function)
        if func:
            func(*args, **kwargs)
    except TypeError as e:
        print(e.args[0])


def main(argv: Optional[List[str]] = None) -> None:
    """Main function.

    Args:
        argv (List[str]): command line arguments.
    """
    parser = argparse.ArgumentParser(
        prog="runp",
        description='Run functions in a file.')
    parser.add_argument(
        'runfile',
        help='file containing the functions')
    parser.add_argument(
        'function',
        nargs='?', help='function to run')
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='list available functions in file'
    )
    parser.add_argument(
        '-d', '--detail',
        help='print function docstring'
    )
    if argv is None:
        argv = sys.argv[1:]
    args = parser.parse_args(argv)

    runfile = Path(args.runfile).resolve()

    if not runfile.is_file():
        print("No such file '{}'".format(args.runfile))
        sys.exit(1)

    imported_vars = load_runfile(runfile)
    functions = filter_vars(imported_vars)

    if args.list:
        print_functions(functions)
        sys.exit(0)

    if args.detail:
        print_function(functions, args.detail)
        sys.exit(0)

    if args.function is None:
        print("No function was selected!")
        sys.exit(1)

    run_function(functions, args.function)


if __name__ == "__main__":
    main(sys.argv[1:])
