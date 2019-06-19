#modified version from Forge and Compiler on Stack Overflow
class mock_input():
    arg = ""
    prompt = ""
    def make_input(self, prompts):
        self.prompt = prompts
        return self.arg

    def change_input(self, args):
        self.arg = args
