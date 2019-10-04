import sys
import re

from erica.batch import *
from erica.test import *


def is_batch_class(name):
    match = re.fullmatch(r"Batch\w+", name)
    return match is not None


def is_test_class(name):
    match = re.fullmatch(r"Test\w+", name)
    return match is not None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("command name required\n")
        sys.exit(1)

    command = sys.argv[1]

    if is_batch_class(command):
        eval(command).main(* sys.argv[2:])
    elif is_test_class(command):
        if len(sys.argv) < 3:
            sys.stderr.write("function name required for test\n")
            sys.exit(1)

        function = sys.argv[2]
        eval(command + "." + function)(* sys.argv[3:])
    else:
        sys.stderr.write("class name is invalid\n")
        sys.exit(1)
