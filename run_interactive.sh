#!/bin/bash

# probably use salloc --time=0-0:10 -A eeb --mem=1G ./run_interactive.sh

module load anaconda3
conda activate gtex-gatk4

base_dir=/projects/AKEY/akey_vol2/serenatu/data/callable_bases/bed/
samples=(LP6005441-DNA_B03 LP6005441-DNA_G10 LP6005592-DNA_A02 LP6005442-DNA_E10 LP6005677-DNA_G01 LP6005443-DNA_B04 LP6005442-DNA_H01 LP6005442-DNA_G09 SS6004477 LP6005592-DNA_D03 LP6005443-DNA_C03)
paths=()
for s in ${samples[@]}; do
    paths+="$base_dir$s/$s.summary.gz "
done
snakemake --use-conda \
    --use-singularity -w 60 \
    -j 5 \
    ${paths[@]}
