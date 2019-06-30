# -*- coding: utf-8 -*-
"""Basic CLI Dork. Test edit."""
import dork.repl as repl


__all__ = ["main"]


def main(*args):
    """Main CLI runner for Dork"""
    script_name = args[0] if args else '???'
    if "-h" in args or '--help' in args:
        print("usage:", script_name, "[-h]")
    else:
        repl.repl()
