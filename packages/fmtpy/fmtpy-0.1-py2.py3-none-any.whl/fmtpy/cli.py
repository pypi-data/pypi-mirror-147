#!/usr/bin/env python
# coding: utf-8

from .fmtpy import main as _main, opts


def main():
    args = opts()
    for file in args.files:
        _main(file, **vars(args))
