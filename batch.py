import sys
import inspect

import erica
from erica.batch import *


if __name__ == "__main__":
    batch_members = inspect.getmembers(erica.batch, inspect.isclass)
    batch_names = [name for name, _ in batch_members]

    if len(sys.argv) < 2:
        for name in batch_names:
            print(name)

        sys.exit(1)

    command = sys.argv[1]

    if command in test_names:
        sys.stderr.write("no such batch command\n")
        sys.exit(1)

    arguments = sys.argv[2:]
    eval(command).main(* arguments)
