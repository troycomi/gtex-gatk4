#!/bin/bash

#set -euo pipefail
#srun --time 0-3 --mem 6G bwa index -a bwtsw /tigress/AKEY/akey_vol1/home/selinav/References.nobackup/hs37d5.fa

module load anaconda3
conda activate gtex-gatk4
PATH=$PATH:/usr/licensed/anaconda3/2019.3/bin

#note on fastq_instances: that step creates temporary unzipped
#fastq files so only run a few to limit disk usage!
#short_jobs are for jobs < 2 hours which are spawned in large numbers. 
#That limits how many jobs are submitted at once to keep the queue clear
#for i in {1..10}; do
snakemake --cluster-config 'della_cluster.yaml' \
    --cluster "sbatch --cpus-per-task={cluster.n} \
                --mem={cluster.memory} --time={cluster.time} \
                --output=slurm_out/%x_%A --job-name={cluster.jobname} \
                --parsable -A eeb" \
    --use-conda \
    --use-singularity -rp -w 60 -j 250 \
    --resources fastq_instances=5 short_jobs=2\
    --max-jobs-per-second 1
#done
    #--restart-times 1
    #--dag | dot -Tsvg > dag.svg
    #--verbose \

# remove all temp files, sometimes if interrupted doesn't get cleaned
#snakemake --delete-temp-output
