import os
from argparse import ArgumentParser, Namespace
from collections import namedtuple
from sys import exit
from typing import NoReturn, Optional

VERSION = "1.1.1"
EnvironmentVariable = namedtuple("EnvironmentVariable", ["name", "value"])


def env_var(var_name: str) -> EnvironmentVariable:
    if (var_value := os.getenv(var_name)) is None:
        raise ValueError  # argparse will catch this and print an error message

    return EnvironmentVariable(var_name, var_value)


def get_pathext() -> list[str]:
    return os.getenv("PATHEXT", "").split(os.path.pathsep)


def get_paths(args: Namespace) -> list[str]:
    if args.path is not None:  # if literal path was specified
        paths = args.path.split(os.pathsep)
        verbose_print(f"Using literal path: {paths}", args.verbose)

    elif args.env is not None:  # if env var was specified
        verbose_print(f"Using environment variable: {args.env.name}", args.verbose)
        paths = args.env.value.split(os.pathsep)
        while "" in paths:
            paths.remove(
                ""
            )  # remove empty string if there is one (e.g if the value ends in a path separator)

    return paths


def verbose_print(msg: str, verbose: bool) -> None:
    if verbose:
        print(msg)


parser = ArgumentParser(description="Search for a file in a list of directories")
parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {VERSION}")
parser.add_argument("file", help="File to search for on the specified path")
parser.add_argument(
    "-pe",
    "--pathext",
    action="store_true",
    default=False,
    help="Look for file with extensions in environment variable PATHEXT "
    "(normally only set on Windows) (default: False)",
)

verbosity_group = parser.add_mutually_exclusive_group()
verbosity_group.add_argument("-v", "--verbose", action="store_true", help="Be verbose")
verbosity_group.add_argument(
    "-q", "--quiet", action="store_true", help="Be quiet (only print found files)"
)

src_group = parser.add_mutually_exclusive_group(required=True)
src_group.add_argument(
    "-p", "--path", help="Literal path to look in (e.g. /usr/bin:/bin:/usr/sbin:/sbin)"
)
src_group.add_argument(
    "-e",
    "--env",
    help="Environment variable to take path to search from (e.g. PATH or LD_LIBRARY_PATH)",
    metavar="VAR",
    type=env_var,  # will call env_var() with the value of the argument
)


def main(args_list: Optional[list[str]] = None) -> int:
    args = parser.parse_args(args_list)  # uses sys.argv[1:] if args is None

    found = False

    for dir in get_paths(args):
        if not os.path.isdir(dir):
            verbose_print(f"Skipping {dir} (not a directory)", args.verbose)
            continue

        full_filepath = os.path.join(dir, args.file)
        filepaths = [full_filepath] + [
            # add extensions if pathext is set
            os.path.join(dir, args.file + ext)
            for ext in get_pathext()
            if args.pathext
        ]
        for filepath in filepaths:
            if os.path.isfile(filepath):
                found = True
                print(
                    f"File '{args.file}' found at '{filepath}'"
                    if not args.quiet
                    else filepath
                )

            else:
                verbose_print(f"File '{args.file}' not found in '{dir}'", args.verbose)

    if not found:
        if not args.quiet:
            print(f"File '{args.file}' not found")
        return 1

    return 0


def real_main() -> NoReturn:
    exit(main())


if __name__ == "__main__":
    real_main()
