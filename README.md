# JobSubmitter

This package is used to submit multple crab or condor tasks on lxplus. Moreover, it is also optimized to produce private Monte-Carlo (MC) samples. 

## Installation

Download the package from git. It is also important to set the crab envinroment as well as CMSSW. 

```bash
git clone https://github.com/dfigueiredo/JobSubmitter.git
```

## Usage

For a given configuration_file.json (specific for condor or crab submission):

```bash
source /cvmfs/cms.cern.ch/common/crab-setup.sh
python SubmitterTool.py --f configuration_file.json
```
There are python scripts which generate template configuration files (*.json).

## Options

```pythonOptions:
  -h, --help            show this help message and exit
  -f FILE, --filename=FILE
                        JSON mapping file
  -p PARSING, --parsing=PARSING
                        parsing: commands which can be passed from SHELL
                        directly. [parsing: --p "submit --file samples.json"]
  -v, --verbose         make lots of noise [default]
```

Therefore, when running the script SubmitterTool.py:

```python
jobs_submission> ?

Documented commands (type help <topic>):
========================================
EOF  exit  help  mode  submit
```

## Changing the Submission Mode

By default, the tool is set to submit with crab.

````python
python SubmitterTool.py --f configuration_condor.json
jobs_submission> mode condor
```

````python
python SubmitterTool.py --f configuration_crab.json
jobs_submission> mode crab
```

## Configuration File

All the configurations are set in a JSON file for condor or crab submission. Multiple task submission can be done.

### Condor

```bash
python createTemplateCondorJson.py
```

```python
{
    "datasets": [
        {
            "executable": "./MissingMassNtupleAnalyzer", 
            "enable": 1, 
            "parameters": [
                "--par1", 
                "--par2" 
            ], 
            "inputfiles": [
                "../file1.txt", 
                "../file2.txt"
            ], 
            "output": "test/", 
            "inputfolder": "/eos/cms/store/group/phys_exotica/PPS-Exo/Grid/Test", 
            "id": 0
        }
    ]
}
```

The options are:

| Monte-Carlo       | Script | Event Content |
| ------------- |:-------------:|-------------:|
| pythia      | source step1-pythia.sh | GEN |
| ExHume      | source step1-exhume.sh | GEN |
| pomwig      | source step1-pomwig.sh | GEN |
| LHE Toy MC   | source step1-LHEGEN.sh | LHE, GEN |

### Crab

A python script is used to produce a template for the crab submission.

```bash
python createTemplateCrabJson.py 
```

```python
{
    "datasets": [
        {
            "eospath": "/store/user/dmf", 
            "enable": 0, 
            "unitsperjob": 250, 
            "localpath": "/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/PrivateMCProduction/PPSMCProduction/working", 
            "lumimask": "", 
            "sample": "", 
            "output": "RunIISummer20UL17GEN.root", 
            "id": 0, 
            "name": "PYTHIA8-SD-TOP-GEN", 
            "parameters": "", 
            "mode": "mc_private_hadron_production", 
            "site": "T2_US_Wisconsin", 
            "input": "", 
            "config": "/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/PrivateMCProduction/PPSMCProduction/working/SD-TOP-PYTHIA8_cfg.py"
        }
     ]
}
```

The options are:

| Monte-Carlo       | Script | Event Content |
| ------------- |:-------------:|-------------:|
| pythia      | source step1-pythia.sh | GEN |
| ExHume      | source step1-exhume.sh | GEN |
| pomwig      | source step1-pomwig.sh | GEN |
| LHE Toy MC   | source step1-LHEGEN.sh | LHE, GEN |
