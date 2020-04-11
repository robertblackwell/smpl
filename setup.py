# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup

# https://coderwall.com/p/qawuyq/use-markdown-readme-s-in-python-modules
import os


def long_desc() :
    # if os.path.exists('README.md'):
    #     long_descr = open('README.md').read()
    # else: 
    #     long_descr = 'Add a fallback short description here'

    with open("README.rst", "rb") as f:
        long_descr = f.read().decode("utf-8")

    return long_descr


long_description = long_desc()


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('pyargs/main.py').read(),
    re.M
    ).group(1)




setup(
    name = "pyargs",
    packages = ["pyargs"],
    entry_points = {
        "console_scripts": ['pyargs = pyargs.main:main']
        },
    version = version,
    description = "A python script to run commands in parallel (think xargs and GNU parallel) without intermixing the output.",
    long_description = long_description,
    
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities'      ],

    keywords='xargs, parallel, cli',

    test_suite="tests.test_pyargs",

    author = "Robert Blackwell",
    author_email = "rob@whiteacorn.com",
    url = "http://github.com/robertoblackwell/pyargs.git",
    license ='MIT',
    zip_safe = False
    )
