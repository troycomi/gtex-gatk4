#!/bin/bash

module load anaconda3
conda activate gtex_gatk4

#note on fastq_instances: that step creates temporary unzipped
#fastq files so only run a few to limit disk usage!
snakemake --cluster-config 'della_cluster.yaml' \
    --cluster "sbatch --cpus-per-task={cluster.n} \
                --mem={cluster.memory} --time={cluster.time} \
                --output=slurm_out/%x_%A --job-name={cluster.jobname} \
                --parsable" \
    --use-singularity -rp -w 60 -j 50 \
    --resources fastq_instances=5
    #--dag | dot -Tsvg > dag.svg
    #--verbose \
