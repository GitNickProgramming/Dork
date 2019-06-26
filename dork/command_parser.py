""" Requires types for Player instance, thanks lint
Python Command parser using dictionaries and Function References
https://www.w3schools.com/python/python_dictionaries.asp -- dictionaries info
https://www.python-course.eu/passing_arguments.php -- info on method reference
https://www.w3schools.com/python/ref_keyword_in.aspThis code will be heavily
commented for descriptive learning purposes.DO NOT DO THIS in production code.
You will be shamed."""
import dork.types
import dork.map_generator


def get_hello_world():
    """Made because of lint liking getters/setters """
    return _hello_world()


def get_goodbye_world():
    """Made because of lint liking getters/setters """
    return _goodbye_world()


def get_show_help():
    """Made because of lint liking getters/setters """
    return _show_help()


def create_player():
    """Really lint? it's what is says on the tin! """
    player = dork.types.Player()
    return player


def _hello_world():
    # return tuple of two values. the second is the repl termination condition
    return "hello, world!", False


def _goodbye_world():
    return "goodbye, world!", True


def _show_help():
    return "try typing 'say hello'", False


def read():
    """Reads input from user.
    """
    return input("> ")


def verify_map(dict):
    """verifies if map is legal"""
    return dork.map_generator.check_data(dict)


def create_map():
    """Makes graph of loaded map"""
    return dork.map_generator.generate_map()


def load_map():
    """Loads map from specified yaml"""
    return dork.map_generator.load_data()


def evaluate(command):
    """Evaluates a command
    """
    # https://docs.python.org/3/library/stdtypes.html#str.split
    if not isinstance(command, str):
        return "Unknown Command", False
    words_in_command = command.split()

    main_menu = {  # look at dictionary notes at top for more info.
        "say": {
            "hello": _hello_world,  # no '()' or else it would call method now
            # read method ref notes at top.
            "goodbye": _goodbye_world,
        },
        "help": {"say": _show_help},
    }

    for verb in words_in_command:
        if verb in main_menu:
            sub_menu = main_menu[verb]
            for subject in words_in_command:
                if subject in sub_menu:
                    function = sub_menu[subject]
                    return function()

    return "Unknown Command", False


def repl():
    """Read eval print loop
    A common idea in terminal command programs
    """
    print("starting repl...")
    while True:
        command = read()
        output, should_exit = evaluate(command)
        print(output)
        if should_exit:
            break
    print("ending repl...")


# https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    repl()
