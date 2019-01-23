from scripts.clean_config import clean_config_paths
from scripts.get_samples import get_samples

configfile: 'subworkflows/config.yaml'

paths = config['path']
paths = clean_config_paths(paths)

ids = glob_wildcards(paths['recal_bam'].replace('{id}', '{id,[^_]+}')).id

# remove ids not found in sample details
sample_details = get_samples(paths['sample_details'])
ids = [id for id in ids if id in sample_details]

subworkflows = config['main']['subworkflows']
if subworkflows is None:
    subworkflows = []

subw_outputs_dict = {}
subw_outputs = []

for subw in set(subworkflows):
    sub_path = 'subworkflows/{}.snake'.format(subw)
    if not os.path.exists(sub_path):
        continue

    subw_outputs_dict[subw] = []

    include: sub_path

    if len(subw_outputs_dict[subw]) == 0:
        continue

    subw_outputs.extend(subw_outputs_dict[subw])

rule all:
    input:
        subworkflow_outputs = subw_outputs

rule clean:
    shell:
        'rm slurm_out/* || echo no slurm output\n'
