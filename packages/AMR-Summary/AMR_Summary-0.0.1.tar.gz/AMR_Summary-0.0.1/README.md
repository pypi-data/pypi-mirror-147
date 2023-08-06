# AMR_Summary

AMR Summary combines the outputs from [ResFinder](https://cge.cbs.dtu.dk/services/ResFinder/) and [MOB-recon](https://github.com/phac-nml/mob-suite) to yield reports with genes AMR resistance phenotypes, and whether they are present on plasmids.

## Installation

AMR_Summary can be installed using conda

Skip this step if you have already installed conda

```
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh;
bash miniconda.sh -b -p $HOME/miniconda
conda update -q conda
```

### Quickstart

You can now install the AMR_Summary package:

`conda install -c olc-bioinformatics amr_summary`

If you encounter the following error:

`PackageNotFoundError: Packages missing in current channels:`

You need to add one or more of the following channels to your conda install:

- conda-forge
- bioconda
- olcbioinformatics

To see which channels you currently have:

```
conda config --show channels
```

To install the missing channel(s)

```
conda config --append channels olcbioinformatics
conda config --append channels conda-forge
conda config --append channels bioconda
```

### Tests

If you encounter issues with the AMR_Summary package, tests are available to ensure that the installation was successful and your credentials are valid.

You will need to clone this repository and run the tests with pytest:


`git clone https://github.com/OLC-Bioinformatics/AMR_Summary.git`

`cd AMR_Summary`

`python -m pytest tests/ --cov=amr_summary -s -vvv`

## Running AMR_Summary
### Arguments

You can be supply absolute, tilde slash, or relative paths or all path arguments

### Required Arguments

- sequence path: name and path of folder containing sequences to process
- database path: name and path of folder containing ResFinder and MOB-recon databases. Note that you do not need to download these databases. The will be downloaded and initialised as part of the script

### Optional Arguments
- report path: name and path of folder in which reports are to be created. Default is sequence_path/reports
- debug: print debug-level logs to console
- version: print version of AMR_Summary

### Example command

To process sequence files in FASTA format in the folder `~/Analyses/sequences`, use databases in `/databases`,  and place reports in your current working directory

`AMR_Summary -s ~/Analyses/sequences -d /databases -r .`

### Usage
```
usage: AMR_Summary [-h] -s  -d  [-r] [--debug] [-v]

AMR Summary: a pipeline to identify AMR resistance genes located on plasmids
by combining ResFinder and MOB-recon

optional arguments:
  -h, --help            show this help message and exit
  -s , --sequence_path 
                        Path of folder containing sequence files in FASTA
                        format to process
  -d , --database_path 
                        Path of folder containing ResFinder and MOB-recon
                        databases. If these databases cannot be located, they
                        will be downloaded
  -r , --report_path    Path of folder in which reports are to be created.
                        Default is sequence_path/reports
  --debug               Enable debug-level messages to be printed to the
                        console
  -v, --version         show program's version number and exit
```