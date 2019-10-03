import sys

from erica.batch import *


if len(sys.argv) < 2:
    sys.stderr.write("command name required\n")
    sys.exit(1)

eval("Batch" + sys.argv[1]).main(* sys.argv[2:])
