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
