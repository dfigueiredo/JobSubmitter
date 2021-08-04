import json
import glob

# Options:
# id (int): identify the key we are submiting.
# enable (bool): to activate/deactivate the crab jobs submission for a given dataset

listing = glob.glob('/eos/cms/store/group/phys_exotica/PPS-Exo/Grid/bjet-data-*/*/*/*/*/*')

data = {}
data['datasets'] = []

year = ''
era = ''
mode = ''
physics = ''
nid = 0

for subdir in listing:

  if '2018A' in subdir:
    era = 'A'
    year = '2018'
  elif '2018B' in subdir:
    era = 'B'
    year = '2018'
  elif '2018C' in subdir:
    era = 'C'
    year = '2018'
  elif '2018D' in subdir:
    era = 'D'
    year = '2018'
  else:
    era = 'NONE'
    year = '2017'
  
  if 'DisplacedJet' in subdir:
    physics = 'displacedjet'
  elif 'BTagMu' in subdir:
    physics = 'bjet'
  elif 'Muon' in subdir:
    physics = 'muon'
  elif 'EGamma' in subdir:
    physics = 'electron'
  else:
    physics = 'NONE'

  if 'data' in subdir:
    mode = 'data'
  elif 'mc' in subdir:
    mode = 'mc'
  else:
    mode = 'NONE'

  data['datasets'].append({
    'id': nid,
    'enable': 1,
    'inputfolder': subdir+"/",
    'executable': "/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/DarkMatterSearch/2021/NTuplizer/CMSSW_10_6_17_patch1/src/PPSFramework/Analyzer/MissingMassNtupleAnalyzer",
    'inputfiles': (""),
    'parameters':("--f $(filename)","--year "+year,"--era "+era,"--mode "+mode,"--physics "+physics,"--jobid $(ProcId)"),
    'output': (physics+"-"+mode+"-era-"+era+"-year-"+year+"-id"+str(nid)+"/")
  })

  nid = nid + 1
  print(json.dumps(data, indent=4))

with open("samples_condor.json", "w") as write_file:
  json.dump(data, write_file, indent = 4)

