import sys
import os
import io
from glob import glob


fnamebase = os.path.split(sys.argv[1])[1].split('_')
fnamebase[0] = os.path.join(
    os.path.split(sys.argv[1])[0],
    fnamebase[0])

existing = glob(f"{fnamebase[0]}_*_{fnamebase[1]}")
if len(existing) > 0:
    for f in sorted(existing):
        print(f + " ")
    sys.exit(0)
