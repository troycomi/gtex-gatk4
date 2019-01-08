import gzip
import sys
import os
import io


writers = {}
fnamebase = os.path.split(sys.argv[1])[1].split('_')
fnamebase[0] = os.path.join(
    os.path.split(sys.argv[1])[0],
    fnamebase[0])

with io.BufferedReader(gzip.open(sys.argv[1], 'rb')) as fastq:
    step = 0
    for l in fastq:
        if step == 0:
            key = str(l)
            key = key.split(' ')[0].split(':')
            key = '_'.join(key[1:3])
            if key not in writers:
                writers[key] = io.BufferedWriter(gzip.open(
                    f"{fnamebase[0]}_{key}_{fnamebase[1]}", 'wb'))
            writer = writers[key]

        writer.write(l)
        step = (step + 1) % 4

    for w in writers.values():
        w.close()

    for k in writers.keys():
        print(f"{fnamebase[0]}_{key}_{fnamebase[1]} ")
