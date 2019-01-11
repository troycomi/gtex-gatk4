#!/bin/bash

# appends seff information for all .out files in the supplied directory
# skips out files that are already processed and running jobs
# usage reportSeff.sh OUT_DIR
# assumes out files are named as NAME_JOB_ARRAY.out, no _ in NAME

set -euo pipefail

if [ "$#" -ne 1 ] || [ -z "$1" ] || [ ! -d $1 ]; then
    echo "Error: expected directory argument"
    echo "Usage: $0 DIRECTORY"
fi

find "$1" -type f -print0 | \
    while IFS= read -r -d '' FILE; do
        JOB=$(basename $FILE)
        JOB=${JOB##*_}

        #test if job is still running
        [[ `squeue -j $JOB 2> /dev/null | grep $JOB` ]] \
            && echo -e "$JOB is still running" && continue 

        #append seff
        echo $FILE 
        seff $JOB 
        echo -e '\n' 
    done
