from scripts.clean_config import clean_config_paths, join_config_paths
from scripts.get_samples import get_samples
import os
from slurm_scrub.predictor import Predictor


predictor = Predictor('slurm_out/training.json')

def est_resource(job, inputs, resource, default, attempt):
    try:
        result = predictor.estimate(job,
                                    sum([os.path.getsize(i) for i in inputs]),
                                    resource, default, attempt)
    except:
        print(f'Error in {job} {resource} {default} for {inputs}')
        raise Exception
    return result

configfile: 'config_wgs.yaml'

paths = config['path']
paths = clean_config_paths(paths)
paths['base'] = os.getcwd()

# sample ids to run workflow with
if 'recal_bam' not in paths:
    configfile: paths['base'] + '/subworkflows/GATK-bqsr.yaml'
    paths = join_config_paths(paths, config['path'])

# sample ids to run workflow with
#ids = glob_wildcards(paths['fastq_R1'].replace('{id}', '{id,[^_]+}')).id
ids = glob_wildcards(paths['recal_bam'].format(id='{id, [^/]+}')).id

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
