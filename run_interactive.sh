#!/bin/bash

# probably use salloc --time=0-0:10 -A eeb --mem=1G ./run_interactive.sh

module load anaconda3
conda activate gtex-gatk4
PATH=$PATH:/usr/licensed/anaconda3/2019.3/bin

snakemake --use-conda \
    --use-singularity -w 60 \
    --resources fastq_instances=5
