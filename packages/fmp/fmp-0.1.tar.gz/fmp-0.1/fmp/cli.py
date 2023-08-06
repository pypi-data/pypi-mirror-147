#!/usr/bin/env python
# coding: utf-8

from .fmp import main as _main, opts


def main():
    args = opts()
    for file in args.files:
        _main(file, **vars(args))
