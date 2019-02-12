# gtex-gatk4
> Snakemake implementation of GATK4 pipeline for GTEx Project
A collection of subworkflows to manage the analysis and variant calling of 
somatic mutations from GTEx samples.

## Installation
The main installation process is the generation of a conda environment with the
following: 
```
conda create -n gtex-gatk4 --file environment.yml
```
The first run of snakemake requires network access to download all docker
images.

## Usage
Snakemake is a workflow definition language, which is difficult to follow if
you are used to a sequential, scripting language.  Instead of defining an order
of execution, rules dictate how to generate an output file from an input file.
The power of snakemake comes from the control over wildcards in filenames to
generalize rules across datasets.  The code organization has a main Snakefile
that reads in subworkflows to generate the workflow required to produce final 
output files.  Subworkflows are collections of rules to accomplish a part of
analysis, e.g. mapping sequences or performing variant calling.  However, 
most of the customization will be in the config.yaml file and the 
della\_cluster.yaml file.

### config.yaml
The config file contains most of the variables controlling execution of the 
workflow.  Each section is discussed further below.

#### subworkflows
Subworkflows lists the analyses which are desired for the snakemake execution. 
The name must match the .snake file in the subworkflows directory exactly.

#### path
Path consists of locations for docker containers along with file names defining
all input and output.  Remember, the flexibility of snakemake is derived from
simply linking filenames to rules to decide what needs to be run.  There is 
limited pattern matching and substitution to reference other paths.  For 
example, "\_\_DATA\_ROOT\_\_/{id}.fastq" will have the value of "data\_root"
substituted for "\_\_DATA\_ROOT\_\_".  Any part of the filenames can be modified
except for wildcards, any part of the filename in braces, e.g. {id} above.

The entries in path are generally organized by subworkflow.  Snakemake will 
exit gracefully if an input file isn't found.

#### gatk
The gatk entry contains all options for each gatk tool used in the workflows.
"memory" refers to the argument passed to java; memory requested from slurm is
covered below.  Additional options are supplied as "options"

#### shearwater
The variables here are more involved and relate to issues of dividing execution
in a meaningful way.  "priors" is a list of prior arguments to pass into bf2vcf

### della\_cluster.yaml 
This yaml file controls sbatch submissions for most steps of the workflow.
Some rules execute within seconds, using negligible memory and are run locally.

The \_\_default\_\_ values are used unless a rule overwrites an option below.
Every other entry matches either a rule name or a group name.  The jobname 
(output to the slurm\_out directory) matches the rule or group name in most
cases.  The chosen values were tuned for the exome sequences of ~400 human 
samples and may not be suitable for other applications.  Always examine seff
information to see if resources need adjustment.

### Execution
With the config.yaml file setup properly, snakemake can be run locally with
simply executing
```
snakemake
```
Debugging and troubleshooting is best done locally using either
```
snakemake -n --quiet
```
to see the rule count and validate the execution path. Or
```
snakemake -npr
```
provides a detailed reason for the rule being run (r) along with the prompt 
which will be executed (p). 

When ready, cluster execution can be performed with the run\_della.sh script.

### Seff Examination
The reportSeff script presents seff information in a formatted table. It takes
the slurmout directory as an argument or uses the current working directory. 
Files that have a job number as the last token after an underscore are analyzed.
A sample usage:
```
./reportSeff.sh slurm_out/
```
Depending on the size of the output, pipe through less or write to an output
file.
