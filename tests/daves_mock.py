"""Hastily made utility for testing raw input
    modified version from Forge and Compiler on Stack Overflow"""


class MockInput():
    """class for any string input """
    arg = ""
    prompt = ""
    def make_input(self, prompts):
        """injects input into builtin input methods"""
        self.prompt = prompts
        return self.arg

    def change_input(self, args):
        """changes mocked input for testing"""
        self.arg = args
