import logging
from scripts.clean_config import clean_config_paths

logging_format = '#%(asctime)s | %(levelname)-7s | %(filename)-20s: %(message)s'
verbosity = str(config.get('verbosity', 'INFO')).upper()

if verbosity not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
    logging.basicConfig(level=logging.INFO, format=logging_format)
    logging.warning("Invalid verbosity specified ('%s')", verbosity)

else:
    logging.basicConfig(level=getattr(logging, verbosity), format=logging_format)

configfile: 'subworkflows/config.yaml'

paths = config['path']
paths = clean_config_paths(paths)

ids = glob_wildcards(paths['fastq_R1'].replace('{id}', '{id,[^_]+}')).id
logging.info("Found {} fastq files to process...".format(len(ids)))

subworkflows = config['main']['subworkflows']
if subworkflows is None:
    subworkflows = []
logging.info("Subworkflows to perform: %s", subworkflows)

subw_outputs_dict = {}
subw_outputs = []

for subw in set(subworkflows):
    sub_path = 'subworkflows/{}.snake'.format(subw)
    if not os.path.exists(sub_path):
        logging.warning('Cannot find workflow %s at %s.  Skipping...',
                        subw,
                        sub_path)
        continue

    subw_outputs_dict[subw] = []

    include: sub_path

    if len(subw_outputs_dict[subw]) == 0:
        logging.warning('No output specified by snakefile %s', subw)
        continue

    subw_outputs.extend(subw_outputs_dict[subw])

logging.info("IDs:")
logging.info(ids)
logging.info('Subworkflow outputs:')
logging.info(subw_outputs)

onstart:
    logging.info('Starting pipeline ...')

rule all:
    input:
        subworkflow_outputs = subw_outputs

    run:
        logging.info('Pipeline completed.')

rule clean:
    shell:
        'rm slurm_out/* || echo no slurm output\n'
