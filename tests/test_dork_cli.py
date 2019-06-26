# -*- coding: utf-8 -*-
"""Basic tests for the dork cli
"""
from types import FunctionType
import dork.cli


def test_cli_exists(run):
    """Dork.cli.main should always exist and run
    """
    assert "main" in vars(dork.cli), "Dork.cli should define a main method"
    assert isinstance(dork.cli.main, FunctionType)
    try:
        run(dork.cli.main)
    except:  # noqa: E722
        raise AssertionError("cannot run 'dork' command")


def test_cli_help(run):
    """CLI's help command should return helpful information
    """
    tupe = run(dork.cli.main, '-h', input_side_effect=[])
    assert 'usage' in tupe[0], "usage output"
