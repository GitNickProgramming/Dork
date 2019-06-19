#modified version from Forge and Compiler on Stack Overflow
class mock_input():
    arg = ""

    def make_input(self):
        return self.arg
    def change_input(self, args):
        self.arg = args
