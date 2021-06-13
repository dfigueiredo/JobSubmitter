# JobSubmitter

This package is used to submit multple crab or condor tasks on lxplus. Moreover, it is also optimized to produce private Monte-Carlo (MC) samples. 

## Installation

Download the package from git. It is also important to set the crab environment as well as CMSSW (cmsenv) where your plugins are set. 

```bash
git clone https://github.com/dfigueiredo/JobSubmitter.git
```

## Usage

For a given configuration_file.json (specific for condor or crab submission):

```bash
source /cvmfs/cms.cern.ch/common/crab-setup.sh
python SubmitterTool.py --f configuration_file.json
```

There are python scripts which generate template configuration files (*.json):

```bash
python createTemplateCondorJson.py
```

```bash
python createTemplateCrabJson.py 
```

## Options

```python
Options:
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

```python
python SubmitterTool.py --f configuration_condor.json
jobs_submission> mode condor
```

```python
python SubmitterTool.py --f configuration_crab.json
jobs_submission> mode crab
```

## Configuration File

All the configurations are set in a JSON file for condor or crab submission. Multiple task submission can be done.

### Condor

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

| Options       | Explanation | Comments |
| ------------- |:-------------:|-------------:|
| executable      | (string) User code |  |
| enable      | (int) 0 or 1 |  |
| parameters      | (vector string) executable options |  |
| inputfiles   | (vector string) auxiliary input files | In case of extra files |
| output   | (string) output folder | Condor output. Automatic created. |
| inputfolder   | (string) multiple root files | Condor will create a job per file (*.root) |
| id   | (int) identifier | Start from 0. Must be different |

### Crab

A python script is used to produce a template for the crab submission.

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

| Options       | Explanation | Comments |
| ------------- |:-------------:|-------------:|
| eospath      | (string) eos or store user area |  |
| enable      | (int) 0 or 1 |  |
| unitsperjob      | (int) number of files per job (MC) or LS units (data) |  |
| localpath   | (string) directory where the crab folder will be saved |
| lumimask   | (string) when running with data | |
| sample   | (string) dataset | Empty for GEN creation (MC) |
| output   | (string) crab root output file | Same name as in the CMSSW config |
| id   | (int) identifier. | Start from 0. Must be different |
| name   | (string) name of the task and name of dataset (when created) | |
| parameters   | (vector string) CMSSW input parameters |  |
| mode   | (string) data_analysis  | For data analysis |
|    | (string) mc_analysis  | For MC analysis |
|    | (string) mc_private_analysis | For MC analysis (DBS phys03) |
|    | (string) mc_private_hadron_production | For MC GEN production (DBS phys03) |
|    | (string) mc_private_hadron_lhe_production | For MC LHE production (DBS phys03) |
| site   | (string) Storage Site | |
| input   | (string) In case of extra input file | |
| config   | (string) CMSSW config file | |

