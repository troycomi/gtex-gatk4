import sys
import os
from glob import glob


writers = {}
fnamebase = os.path.split(sys.argv[1])[1].split('_')
fnamebase[0] = os.path.join(
    os.path.split(sys.argv[2])[0],
    fnamebase[0])
fnamebase[1] = os.path.splitext(fnamebase[1])[0]  # remove gz

# exit early if there are existing files (does not check for partial files!)
existing = glob(f"{fnamebase[0]}_*_{fnamebase[1]}")
if len(existing) > 0:
    sys.exit(0)

step = 0
for l in sys.stdin:
    if step == 0:
        key = l
        key = key.split(' ')[0].split(':')
        key = '_'.join(key[1:3])
        if key not in writers:
            writers[key] = open(
                f"{fnamebase[0]}_{key}_{fnamebase[1]}", 'w')
        writer = writers[key]

    writer.write(l)
    step = (step + 1) % 4

for w in writers.values():
    w.close()
