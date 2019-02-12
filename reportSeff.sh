#!/bin/bash

# appends seff information for all .out files in the supplied directory
# skips out files that are already processed and running jobs
# usage reportSeff.sh OUT_DIR
# assumes out files are named as NAME_JOB_ARRAY.out, no _ in NAME

if [ "$#" -ne 1 ] || [ -z "$1" ] || [ ! -d $1 ]; then
    DIR=$(pwd)
else
    DIR=$1
fi

printf "%12s%6s%12s\t%-15s%-10s%-15s%s\n" "" Job "" State CPU Time Memory
find "$DIR" -maxdepth 1 -type f -regex '.*_[0-9][0-9]*$' -print0 | sort -z | \
    while IFS= read -r -d '' FILE; do
        JOB=$(basename $FILE)
        JOB=${JOB##*_}

        #test if job is still running
        [[ `squeue -j $JOB 2> /dev/null | grep $JOB` ]] \
            && continue 

        #append seff
        printf "%30s\t" $(basename $FILE)
        awk '
        /State:/{printf "%-15s", $2}
        /CPU Eff/{printf "%-10s", $3}
        /Job Wall/{printf "%-15s", $4}
        /Memory Eff/{printf "%s %s %s %s\n", $3, $4, $5, $6}
        ' <(seff $JOB)
    done
