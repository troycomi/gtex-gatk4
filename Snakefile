from scripts.clean_config import clean_config_paths, join_config_paths
from scripts.get_samples import get_samples
import os

#configfile: 'config_wgs.yaml'
configfile: 'config.yaml'

paths = config['path']
paths = clean_config_paths(paths)
paths['base'] = os.getcwd()

ids = {}
valid_chromosomes = {str(c) for c in range(1,23)}
# sample ids to run workflow with
for dirname in paths['input_dirs']:
    wc = glob_wildcards(dirname + paths['bam_pattern'].split('/')[1])  # strip leading id dir
    for chrom in set(wc.chromosome):
        if chrom not in valid_chromosomes:
            #raise ValueError(f'Unexpected chromosome {chrom} in {dirname}')
            pass
    wc_id = [w.split('/')[1] for w in wc.id]
    for id in set(wc_id):
        chroms = {ch for i, ch in zip(wc_id, wc.chromosome)
                  if id == i}
        if valid_chromosomes - chroms:
            print(dirname)
            print(f"sample {id} missing {len(valid_chromosomes - chroms)} chromosomes")
            # print(f"{sorted(valid_chromosomes - chroms)}")
        else:
            ids[id] = dirname + paths['bam_pattern']

# i = list(ids.keys())[0]
# ids = {i: ids[i]}
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
    shell("echo 'Check error log' | mail -s 'gatk-stucci error' tcomi@princeton.edu")
    print("Done")

localrules:
    all

rule all:
    input:
        subworkflow_outputs = subw_outputs

rule clean:
    shell:
        'rm slurm_out/* || echo no slurm output\n'
