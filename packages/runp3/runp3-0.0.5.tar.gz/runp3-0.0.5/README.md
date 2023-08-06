# runp

[![Python package](https://github.com/TakashiKusachi/runp3/actions/workflows/python-package.yml/badge.svg )](https://github.com/TakashiKusachi/runp3/actions/workflows/python-package.yml) [![Coverage Status](https://coveralls.io/repos/github/TakashiKusachi/runp3/badge.svg?branch=master)](https://coveralls.io/github/TakashiKusachi/runp3?branch=master) [![PyPI version](https://badge.fury.io/py/runp3.svg )](https://badge.fury.io/py/runp3) [![Python Versions](https://img.shields.io/pypi/pyversions/runp3.svg )](https://pypi.org/project/runp3/)


This repository is a modified of runp, which is no longer maintained, for modern Python 3.

runp exports Python functions from files to the command line. 
You don't need to change your existing code.

If you have a file named myfile.py with::

    def foo():
        """beeps a lot"""
        print "beep beep"

    def bar(text):
        """Prints things

        Args:
            text (str): The text to print
        """
        print text

And you want to run it in the command line just do::

    $ runp myfile.py foo
    beep beep

You can also pass arguments to your functions::

    $ runp myfile.py bar:"this is sweet!"
    this is sweet!

Functions with names starting with _ are hidden. 

You can list available functions with::

    $ runp myfile.py -l
    Available functions:
    foo    beeps a lot
    bar    Prints things

And get info on a specific function::

    $ runp myfile.py -d bar
    Displaying docstring for function bar in module myfile

    bar(text)
        Prints things
    
        Args:
            text (str): The text to print

Syntax for calling functions is::
    
    $ runp myfile.py function_name:arg1value,arg2=arg2value


The concept, syntax for commands and initial code are heavily inspired by fabric's task system.
