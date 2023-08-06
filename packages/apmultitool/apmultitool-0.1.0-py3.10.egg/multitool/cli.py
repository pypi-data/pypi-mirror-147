import argparse
import sys

from multitool.runner import binprint, contains, synonyms, wordle


def execute(args=None):
    """
    Operate the main function for program.
    """
    if not args:
        args = sys.argv

    if len(args) <= 1:
        args.append("-h")

    parser = argparse.ArgumentParser(
        "multitool", description="Multitool CLI", prefix_chars="-"
    )

    parsers = parser.add_subparsers()

    binparser = parsers.add_parser("bin", help="Convert integers to binary")

    binparser.add_argument("value", help="Integer to convert", action="store")

    binparser.set_defaults(func=binprint)

    synparse = parsers.add_parser("syn", help="get synonyms for commong words")

    synparse.add_argument(
        "word",
        help="Show Synonyms for the word",
        action="store",
        metavar="<word>",
    )

    synparse.add_argument(
        "-p",
        "--precision",
        help="how many similar words to include with the original.",
        dest="precision",
        action="store",
        metavar="<n>",
        default="1",
    )

    synparse.set_defaults(func=synonyms)

    containsparser = parsers.add_parser(
        "contains", help="Show words that contain <text>."
    )

    containsparser.add_argument(
        "--start",
        help="Show words that start with <text>",
        dest="start",
        metavar="<text>",
        action="store",
    )

    containsparser.add_argument(
        "--end",
        help="Show words that end with <text>",
        dest="end",
        metavar="<text>",
        action="store",
    )

    containsparser.add_argument(
        "-l",
        "--length",
        help="number <n> of characters in word",
        dest="length",
        metavar="<n>",
        action="store",
    )

    containsparser.set_defaults(func=contains)

    wordleparser = parsers.add_parser("wordle", help="wordle helper tool")

    wordleparser.set_defaults(func=wordle)

    wordleparser.add_argument(
        "-g", "--gui", action="store_true", help="use gui", dest="gui"
    )

    wordleparser.add_argument(
        "-s",
        "--size",
        action="store",
        help="The number of letters in the word puzzle (default 5)",
        default="5",
        dest="size",
        metavar="<int>",
    )

    utfparser = parsers.add_parser("utf", help="print unicode characters to terminal")

    utfparser.add_argument(
        "number",
        help="one or more space seperated utf-8 codepoint(s)",
        nargs="?",
        action="store",
        default="None",
    )

    utfparser.add_argument(
        "-r", "--range", nargs=2, metavar="<number>", dest="range", action="store"
    )

    namespace = parser.parse_args(args[1:])

    if namespace:
        print(namespace)
        namespace.func(namespace)
    return
