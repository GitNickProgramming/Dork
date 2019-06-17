

def read():
    """Reads input from user.
    """
    return input("> ")


def _evaluate(command):
    """Evaluates a command
    """
    pass

def repl():
    """Read eval print loop
    A common idea in terminal command programs
    """
    print("starting repl...")
    while True:
        output, should_exit = evaluate(read())
        print(output)
        if should_exit:
            break
    print("ending repl...")


# https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    repl()
