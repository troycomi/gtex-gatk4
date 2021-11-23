from scripts.clean_config import clean_config_paths, join_config_paths
from scripts.get_samples import get_samples
import os


# configfile: 'config_wgs.yaml'
configfile: 'config.yaml'

paths = config['path']
paths = clean_config_paths(paths)
paths['base'] = os.getcwd()

# sample ids to run workflow with
if 'recal_bam' not in paths:
    configfile: paths['base'] + '/subworkflows/GATK-bqsr.yaml'
    paths = join_config_paths(paths, config['path'])

ids = []  # glob_wildcards(paths['recal_bam'].format(id='{id, [^/]+}')).id

if len(ids) == 0:  # no recal bams yet
    ids = [line.split()[1]
            for line in open(paths['sample_details'], 'r')
            ]
    ids = ids[1:]  # remove header

# remove contaminated samples
# ids = [i for i in ids if i not in ('P6-B6', 'P6-A4')]

chromosomes = list(range(1,23))

print(f"found {len(ids)} samples to process")

subworkflows = config['main']['subworkflows']
if subworkflows is None:
    subworkflows = []

subw_outputs_dict = {}
subw_outputs = []

for subw in subworkflows:
    sub_path = 'subworkflows/{}.snake'.format(subw)
    sub_config = 'subworkflows/{}.yaml'.format(subw)
    if not os.path.exists(sub_path):
        print(f'skipping {subw}, files not found')
        continue

    subw_outputs_dict[subw] = []

    if os.path.exists(sub_config):
        configfile: sub_config
        paths = join_config_paths(paths, config['path'])

    include: sub_path

    if len(subw_outputs_dict[subw]) == 0:
        continue

    subw_outputs.extend(subw_outputs_dict[subw])

onstart:
    print(f"{len(ids)} samples found...")

onerror:
    print("Error! Mailing log...")
    shell("tail -n 100 {log} | mail -s 'gtex-gatk error' tcomi@princeton.edu")
    print("Done")

localrules:
    all

rule all:
    input:
        subworkflow_outputs = subw_outputs

rule clean:
    shell:
        'rm slurm_out/* || echo no slurm output\n'
