"""
Python Command parser using dictionaries and Function References
https://www.w3schools.com/python/python_dictionaries.asp -- dictionaries info
https://www.python-course.eu/passing_arguments.php -- info on method reference
https://www.w3schools.com/python/ref_keyword_in.asp -- info on keyword `in'
This code will be heavily commented for descriptive learning purposes.
DO NOT DO THIS in production code. You will be shamed.

private methods:
if a function/method starts with a `_' it is considered private by python.
There no need to document private methods as they tend to change frequently
"""

from functools import partial


def _hello_world():
    # return tuple of two values. the second is the repl termination condition
    return "hello, world!", False


def _goodbye_world():
    return "goodbye, world!", True


def _show_help():
    return "try typing 'say hello'", False


def _move_help():
    return "try typing 'go north'", False


def _exit_help():
    return "try typing 'say goodbye'", False


def _move(cardinal):
    return f"You moved to the {cardinal}", False


def read():
    """Reads input from user.
    """
    return input("> ")


def evaluate(command):
    """Evaluates a command
    """
    # https://docs.python.org/3/library/stdtypes.html#str.split
    words_in_command = command.split()

    main_menu = {  # look at dictionary notes at top for more info.
        "say": {
            "hello": _hello_world,  # no '()' or else it would call method now
            # read method ref notes at top.
            "goodbye": _goodbye_world,
        },
        "move": {
            "north": partial(_move, "north"),
            "south": partial(_move, "south"),
            "east": partial(_move, "east"),
            "west": partial(_move, "west"),
            "n": partial(_move, "north"),
            "s": partial(_move, "south"),
            "e": partial(_move, "east"),
            "w": partial(_move, "west")
        },
        "go": {
            "north": partial(_move, "north"),
            "south": partial(_move, "south"),
            "east": partial(_move, "east"),
            "west": partial(_move, "west"),
            "n": partial(_move, "north"),
            "s": partial(_move, "south"),
            "e": partial(_move, "east"),
            "w": partial(_move, "west")
        },
        "help": {
            "say": _show_help,
            "move": _move_help,
            "exit": _exit_help
        },
    }

    for word in words_in_command:
        if word in main_menu:
            sub_menu = main_menu[word]
            for word in words_in_command:
                if word in sub_menu:
                    function = sub_menu[word]
                    return function()

    return "Unknown Command", False


def repl():
    """Read eval print loop
    A common idea in terminal command programs
    """
    print("starting repl...")
    while True:
        # command = read()
        output, should_exit = evaluate(read())
        print(output)
        if should_exit:
            break
    print("ending repl...")


# https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    repl()
