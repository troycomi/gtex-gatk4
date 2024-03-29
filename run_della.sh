#!/bin/bash

#set -euo pipefail
#srun --time 0-3 --mem 6G bwa index -a bwtsw /tigress/AKEY/akey_vol1/home/selinav/References.nobackup/hs37d5.fa

module load anaconda3/2019.3
conda activate gtex-gatk4
PATH=$PATH:/usr/licensed/anaconda3/2019.3/bin

#note on fastq_instances: that step creates temporary unzipped
#fastq files so only run a few to limit disk usage!
#short_jobs are for jobs < 1 hour which are spawned in large numbers.
#That limits how many jobs are submitted at once to keep the queue clear
snakemake \
    --cluster "sbatch --cpus-per-task={threads} \
                --mem={resources.mem}M --time={resources.time} \
                --output=slurm_out/%x_%A --job-name={rule} \
                --parsable -A eeb" \
    --cluster-status "/home/tcomi/scripts/slurm-status.py" \
    --local-cores 5 \
    --use-conda \
    --use-singularity -w 120 -j 250 \
    --resources fastq_instances=10 short_jobs=10 aspera_downloads=5 aria_downloads=10 \
    --max-jobs-per-second 1 \
    --rerun-incomplete \
    -p \
    $@
    # --keep-going \
    # --restart-times 1

    #--dag | dot -Tsvg > dag.svg
    #--verbose \

# remove all temp files, sometimes if interrupted doesn't get cleaned
#snakemake --delete-temp-output
