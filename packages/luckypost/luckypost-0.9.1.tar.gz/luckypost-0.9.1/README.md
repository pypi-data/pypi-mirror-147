# Luckypost

A luckypost is a compact human-readable text-based data structure designed for
decentralized and trust-less authenticated public text-based discussion.

This is a Python library for creating, parsing and verifying luckyposts, it also
provides a basic command-line interface. 

This library is intended to be used by luckynet clients.


# Installation

You'll need a Python interpreter along with the pip package installer.

`python -m pip install luckypost`


# Usage

A command-line interface is provided to access the library's functionality, this
is intended for luckynet developers, not users (but users are welcome to use 
it if they want).

## Hello world
`python -m luckypost en.test authorname "<Hello world!"`

The user will then be prompted to enter their passphrase, alternatively it can
be specified on the command line with the `-p` argument.