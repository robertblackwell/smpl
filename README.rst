pyargs, Python Args Utility
===========================

Version: 0.13.0

``pyargs`` is a python cli program to run a series of scripts or
commands using multiple set or arguments provided from a file or stdin
and to use more than one process to achieve some parallel execution.

The name is deliberately a play on ``xargs`` as pyargs is a simplified
alternative to ``xargs``.

The motivation for this project was to get parallel execution of
commands where the output from each command invocation is kept in a
contigous block rather than being intermixed.

To make for easy replacement of ``xargs`` in existing scripts I used the
same general usage pattern as ``xargs`` and kept of few of the option
short names the same.

I should offer an apology to the **python** community. This is my first
python effort so there is probably a lot in this small project the is no
very ***pythonic***.

See the `github repo <https://github.com/robertblackwell/pyargs>`__.

Usage
-----

::

    usage: wg-runner.py [-h] [-v] [--in INFILE_PATH] [--out OUTFILE_PATH]
                        [-n NARGS] [-P NPROCS] [--stream] [--debug] [--mark]
                        [--lines]
                        cmd [cmd_args [cmd_args ...]]

    Runs multiple instances of a command in parallel with different arguments.
    Think xargs.

    positional arguments:
      cmd                   Command to execute
      cmd_args              Arguments for command to be used for every execution.
                            If any of these are options like -c you might have to
                            enclose them in quotes.

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         Prints the version number.
      --in INFILE_PATH      Path to input file, each line has arguments for
                            command. If not provided uses stdin.
      --out OUTFILE_PATH    Path to output from all commands go to this file path.
                            If not provided stdout.
      -n NARGS, --nargs NARGS
                            Number of args to be found on each line of infile,
                            default = 1.
      -P NPROCS, --nprocs NPROCS
                            Number of parallel process, default = 1.
      --stream              Treat input as a single string rather than a series of
                            line for the purposes of tokenizing into arguments
      --debug               Prints out the command to be executed rather than
                            execute the command, to help problem solve
      --mark, -m            Put markers in the output to make visible the start
                            and output of each command.
      --lines, -L           Send the output line by line rather than keep output
                            frm each execution together.

Install
-------

Using ``pip``

::

    pip install pyargs

Alternatively download or clone the `github
repo <https://github.com/robertblackwell/pyargs>`__ and from the project
directory

::

    python setup.py install

Testing
-------

Pythonic testing is via

::

    python setup.py test

There are only two test cases each of which reside in the
``tests/test_pyargs.py``. These tests cases execute shell scripts

::

    ./tests/end_to_end_test.sh

and

::

    ./tests/writer_to_reader_test.sh

./tests/end_to_end_test.sh
~~~~~~~~~~~~~~~~~~~~~~~~~~

This script executes multiple instances of ``./tests/writer_cmd.py``
using ``pyargs`` with arguments provided from ``tests/test_args``. The
output is piped into, and inspected by ``tests/reader_cmd.py`` which
parses that output and verifies that it is as expected.

./tests/writer_to_reader_test.sh
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pipes the output form ``writer_cmd.py`` into ``reader_cmd.py`` to ensure
that the previous test is using valid test data.

Command options - a bit more detail
-----------------------------------

The options ``--debug``, ``--mark``, ``--lines`` maybe require a little
more explanation.

The script ``./tests/ping_example.sh`` demonstrates the ``--line`` and
``--mark`` options, and ``./tests/ping_example_nl_m.sh`` demonstrates
the ``--mark`` option without ``--lines``.

-  –debug

   When set ``pyargs`` does not execute the commands but rather outputs
   the full command that would have been executed. This enables a user
   to see how ``pyargs`` has interpreted its options and input. This
   option can be helpful in debugging commands that fail.

-  –lines

   The original motivation for ``pyargs`` was to keep all the output
   from a single command invocation in a single contiguous block.
   However this may not always be necessary so this option allows or
   requires that ``pyargs`` will print each line of output from command
   invocations as soon as possible without waiting for the command to
   complete. This means that lines from different command invocations
   can be intermixed. Though **note** that concurrent output is still
   coordinated to ensure that lines do not corrupt each other.

   In order that each line of output can be attributed to the command
   that created it, in this mode, each output line is prefixed with the
   command string of the command that caused the output.

-  –mark

   Sometimes it is difficult to be sure that the output from different
   command invocations have not intermixed (this is when –list is NOT
   set), particularly when many commands are being executed and each
   command generates a lot of output.

   To assist users examine such a situation the \`\ ``--mark`` options
   is provided.

   When ``--mark`` is set ``pyargs`` will modify the output in the
   following manner:

   -  just before the execution of a command instance starts ``pyargs``
      will output a string like

      ::

          MARK: <the command string to be executed> ===================

   -  the output from each command invocation will be bracketed (that is
      have a additional marker line before and after the actual command
      output). This lines will look like this:

      ::

          START OUTPUT[<command string>]

          ...... output lines in here

          END OUTPUT[<command string>]

      These lines (between and including START and END) should be
      contiguous and should be the output from only one command and that
      command should be the one identified in the START and END lines
      (which or course should be the same command). If any of this is
      not the case you have found a bug in ``pyargs``.

Examples
--------

The two scripts ``tests/ping_example.sh`` and ``tests/curl_example.sh``
demonstrate the usage of ``pyargs``.

Note that both these examples attempt to contact hosts/urls that do not
exist and will hence timeout. Hence the output include error messages.
