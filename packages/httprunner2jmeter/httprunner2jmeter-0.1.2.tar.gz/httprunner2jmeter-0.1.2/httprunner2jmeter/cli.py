import argparse
import sys

from loguru import logger

from httprunner2jmeter import __description__, __version__
from httprunner2jmeter.make import main_make

def main():
    """ API test: parse command line options and run commands.
    """
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        "-v", "--version", dest="version", action="store_true", help="show version"
    )
    parser.add_argument(
        "testcase_path", nargs="*", help="Specify YAML/JSON testcase file/folder path"
    )

    args = parser.parse_args()
    if args.version:
        # httprunner
        print(f"{__version__}")
        sys.exit(0)
    elif not args.testcase_path:
        parser.print_help()
        sys.exit(0)
    else:
        main_make(args.testcase_path)
