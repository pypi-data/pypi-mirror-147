import os
import atexit
import inspect
import argparse
import docstring_parser


def start(func):
    """"Decorator to make a main function that accepts command-line arguments"""
    # Check that the caller is being ran as script
    caller_name = inspect.stack()[1].frame.f_locals["__name__"]
    if caller_name == "__main__":
        # Run the function when the script would otherwise finish, so that a 'def main()' at the top
        # can call functions below, like having 'if __name__ == "__main__"' at bottom allows
        atexit.register(lambda: _run(func))

    # Return the function so that it can still be called manually
    return func


def _run(func):
    try:
        # Parse arguments based on function signature
        parser, positional_only = _construct_parser(func)
        all_arguments = vars(parser.parse_args()).items()

        # Run function with those arguments
        args = [value for name, value in all_arguments if name in positional_only]
        kwargs = {name: value for name, value in all_arguments if name not in positional_only}
        func(*args, **kwargs)
    except SystemExit as e:
        # Escalate normal sys.exit (which doesn't work in atexit functions)
        os._exit(e.code)


def _construct_parser(func):
    # Get function signature and docstring
    signature = inspect.signature(func)
    signature_params = signature.parameters.items()

    docstring = docstring_parser.parse(func.__doc__)
    docstring_params = docstring.params

    parser = argparse.ArgumentParser(description=docstring.short_description,
                                     epilog=docstring.long_description)

    # Cycle through params, adding to arg parser
    positional_only = []
    for name, value in signature_params:
        # Find param description from docstring
        docstring_param = [param for param in docstring_params if param.arg_name == name]
        description = docstring_param[0].description if len(docstring_param) > 0 else ""
        name = value.name.replace("_", "-")

        # Construct argument parser add_argument arguments (arg!)
        arg_args = {"help": description}
        if value.annotation != inspect._empty:
            arg_args["type"] = value.annotation

        kind = inspect._PARAM_NAME_MAPPING[value.kind]

        # Keep track of positional-only, since they can't be passed in to function as dict
        if kind == "positional-only":
            positional_only.append(name)

        # Variadic arguments (*args, **kwargs)
        if kind == "variadic positional":
            parser.add_argument(name, **arg_args, nargs="*")

        elif kind == "variadic keyword":
            parser.add_argument("-" + _acronym(name), "--" + name, **arg_args, nargs="*")

        # Has no default value: Create positional argument unless it's keyword-only
        elif value.default == inspect._empty:
            if kind == "keyword-only":
                parser.add_argument("-" + _acronym(name), "--" + name, **arg_args, required=True)
            else:
                parser.add_argument(name, **arg_args)

        # Bool: Create --toggle-flag requiring no value specified after
        elif kind == "positional or keyword" and type(value.default) == bool:
            parser.add_argument("-" + _acronym(name), "--" + name, **arg_args,
                                action="store_false" if value.default else "store_true")

        # Has default value: Create --flag argument unless it's positional-only
        else:
            arg_args["default"] = value.default
            arg_args["type"] = type(value.default)
            if kind == "positional-only":
                parser.add_argument(name, **arg_args, nargs="?")
            else:
                parser.add_argument("-" + _acronym(name), "--" + name, **arg_args)

    return parser, positional_only


def _acronym(name, already_used_cache=[]):
    acronym = name[0]
    prev_letter = None
    for letter in name:
        if letter.isupper() or prev_letter == "-":
            acronym += letter.lower()
        prev_letter = letter

    # Append number if acronym conflicts
    acronym_safe = acronym
    i = 1
    while acronym_safe in already_used_cache:
        i += 1
        acronym_safe = f"{acronym}{i}"

    already_used_cache.append(acronym_safe)
    return acronym_safe
