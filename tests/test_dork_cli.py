# -*- coding: utf-8 -*-
"""Basic tests for the dork cli"""
from types import FunctionType
# from unittest import mock
import dork.cli


def test_cli_exists():
    """Dork.cli.main should always exist and runs
    """
    assert "main" in vars(dork.cli), "Dork.cli should define a main method"
    assert isinstance(dork.cli.main, FunctionType)


def test_cli_help(run):
    """CLI's help command should return helpful information
    """
    out, err, mocked_input = run(dork.cli.main, "-h")
    assert "usage:" in out
    assert err == ""
    assert mocked_input.call_count == 0


def test_cli_unknown(run):
    """Tests CLI's ability to handle unknown args"""
    out, err, mocked_input = run(dork.cli.main, '-?', input_side_effect=['tester', '.rq'])
    assert 'Greetings' in out
    assert err == ""
    assert mocked_input.call_count == 2
