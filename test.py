import sys
import inspect

import erica
from erica.test import *


if __name__ == "__main__":
    test_members = inspect.getmembers(erica.test, inspect.isclass)
    test_names = [name for name, _ in test_members]

    if len(sys.argv) < 2:
        max_length = max([len(x) for x in test_names])

        for name, class_ in test_members:
            for i, method in enumerate(class_.methods):
                if i == 0:
                    print(("{0:" + str(max_length) + "s} {1}").format(name, method))
                else:
                    print((" " * max_length + " " + method))

        sys.exit(1)

    if len(sys.argv) < 3:
        sys.stderr.write("few arguments\n")
        sys.exit(1)

    command = sys.argv[1]

    if command not in test_names:
        sys.stderr.write("no such test command\n")
        sys.exit(1)

    function = sys.argv[2]
    arguments = sys.argv[3:]
    eval(command + "." + function)(* arguments)
