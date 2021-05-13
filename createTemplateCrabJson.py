import json

# Options:
# id (int): identify the key we are submiting.
# enable (bool): to activate/deactivate the crab jobs submission for a given dataset
# localpath: user local area for submission
# eospath: user eos area for submission
# sample: name of the dataset (for mode data_analysis or mc_analysis). For mc_private_production is the name of the datset will be created.
# mode: data_analysis (for Lumimask file), mc_analysis (for eventbased submission) and mc_private_production (for MC production)
# lumimask: only used for data_analysis. Irrelevant for other modes. 
# config: CMSSW config file.
# parameters: parameters of the CMSSW config file.
#      i.e: 'parameters':["--Mode=Muons", "--Era=B"] or 'parameters':[""]
# output: name of the output file.
# unitsperjob: number of unitsperjob per job (for mc_analysis) or number of unitsperjob per NJOBS (for mc_private_production). NJOBS is hardcoded in gridtool library.
# site: 'T2_BR_SPRACE', T2_IT_Pisa, T2_CH_CERNBOX, T2_US_Wisconsin, T2_BR_UERJ

data = {}
data['datasets'] = []

data['datasets'].append({
    'id': 0,
    'enable': 0,
    'localpath': "/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/PrivateMCProduction/PPSMCProduction/working",
    'eospath': "/store/user/dmf",
    'name': "PYTHIA8-SD-TOP-GEN",
    'sample': "",
    'mode': "mc_private_hadron_production",
    'lumimask': "",
    'config': "/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/PrivateMCProduction/PPSMCProduction/working/SD-TOP-PYTHIA8_cfg.py",
    'parameters':(""),
    'input': (""),
    'output': ("RunIISummer20UL17GEN.root"),
    'unitsperjob': 250,
    'site': "T2_US_Wisconsin",
})

data['datasets'].append({
    'id': 1,
    'enable': 0,
    'localpath': "/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/PrivateMCProduction/PPSMCProduction/working",
    'eospath': "/store/user/dmf",
    'name': "PYTHIA8-SD-TOP-GEN-SIM-13TEV",
    'sample': "/PYTHIA8-SD-TOP-GEN/dmf-crab_crab_dmf_2021-04-23_UTC20-01-50-90b9c105ac810048514e168d042afef5/USER",
    'mode': "mc_private_production",
    'lumimask': "",
    'config': "/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/PrivateMCProduction/PPSMCProduction/working/RunIISummer20UL17SIM_cfg.py",
    'parameters':(""),
    'input': (""),
    'output': ("RunIISummer20UL17SIM.root"),
    'unitsperjob': 1,
    'site': "T2_US_Wisconsin",
})

data['datasets'].append({
    'id': 2,
    'enable': 0,
    'localpath': "/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/PrivateMCProduction/PPSMCProduction/working",
    'eospath': "/store/user/dmf",
    'name': "PYTHIA8-SD-TOP-DIGI-PREMIX-13TEV",
    'sample': "/PYTHIA8-SD-TOP-GEN/dmf-PYTHIA8-SD-TOP-GEN-SIM-13TEV-9ac963e13542f33a83ae9ec7fd4ed8d4/USER",
    'mode': "mc_private_production",
    'lumimask': "",
    'config': "/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/PrivateMCProduction/PPSMCProduction/working/RunIISummer20UL17DIGIPremix_cfg.py",
    'parameters':(),
    'input': (""),
    'output':("TOP-RunIISummer20UL17DIGIPremix.root"),
    'unitsperjob': 1,
    'site': "T2_US_Wisconsin",
})

data['datasets'].append({
    'id': 3,
    'enable': 0,
    'localpath': "/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/PrivateMCProduction/PPSMCProduction/working",
    'eospath': "/store/user/dmf",
    'name': "PYTHIA8-SD-TOP-HLT-13TEV",
    'sample': "/PYTHIA8-SD-TOP-GEN/dmf-PYTHIA8-SD-TOP-DIGI-PREMIX-13TEV-1a28be96f8c2ebca4e8c73b389c5e19a/USER",
    'mode': "mc_private_production",
    'lumimask': "",
    'config': "/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/PrivateMCProduction/PPSMCProduction/working/RunIISummer20UL17HLT_cfg.py",
    'parameters':(""),
    'input': (""),
    'output': ("RunIISummer20UL17HLT.root"),
    'unitsperjob': 1,
    'site': "T2_US_Wisconsin",
})

data['datasets'].append({
    'id': 4,
    'enable': 0,
    'localpath': "/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/PrivateMCProduction/PPSMCProduction/working",
    'eospath': "/store/user/dmf",
    'name': "PYTHIA8-SD-TOP-RECO-13TEV",
    'sample': "/PYTHIA8-SD-TOP-GEN/dmf-PYTHIA8-SD-TOP-HLT-13TEV-1cba7fad1227c919886864247a60b1e3/USER",
    'mode': "mc_private_production",
    'lumimask': "",
    'config': "/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/PrivateMCProduction/PPSMCProduction/working/RunIISummer20UL17RECO_cfg.py",
    'parameters':(""),
    'input': (""),
    'output': ("RunIISummer20UL17RECO.root"),
    'unitsperjob': 1,
    'site': "T2_US_Wisconsin",
})

data['datasets'].append({
    'id': 5,
    'enable': 0,
    'localpath': "/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/PrivateMCProduction/PPSMCProduction/working",
    'eospath': "/store/user/dmf",
    'name': "PYTHIA8-SD-TOP-MINIAOD-13TEV",
    'sample': "/PYTHIA8-SD-TOP-GEN/dmf-PYTHIA8-SD-TOP-RECO-13TEV-586b03e1195149d852222d5063e2a23c/USER",
    'mode': "mc_private_production",
    'lumimask': "",
    'config': "/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/PrivateMCProduction/PPSMCProduction/working/RunIISummer20UL17MiniAOD_cfg.py",
    'parameters':(""),
    'input': (""),
    'output': ("RunIISummer20UL17MiniAOD.root"),
    'unitsperjob': 1,
    'site': "T2_US_Wisconsin",
})

data['datasets'].append({
    'id': 6,
    'enable': 0,
    'localpath': "/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/PrivateMCProduction/PPSMCProduction/working",
    'eospath': "/store/user/dmf",
    'name': "PYTHIA8-SD-TOP-MINIAOD-withpps-13TEV",
    'sample': "/PYTHIA8-SD-TOP-GEN/dmf-PYTHIA8-SD-TOP-MINIAOD-13TEV-e67f9b5d033cede4d000433a2a96d4fb/USER",
    'mode': "mc_private_production",
    'lumimask': "",
    'config': "/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/PrivateMCProduction/PPSMCProduction/working/PPS-Objects.py",
    'parameters':("era=B", "year=2017"),
    'input': ("/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/PrivateMCProduction/PPSMCProduction/working/CrossingAngles2016.root","/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/PrivateMCProduction/PPSMCProduction/working/CrossingAngles2017.root","/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/PrivateMCProduction/PPSMCProduction/working/CrossingAngles2018.root"),
    'output':("output.root"),
    'unitsperjob': 1,
    'site': "T2_US_Wisconsin",
})

data['datasets'].append({
    'id': 7,
    'enable': 1,
    'localpath': "/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/DarkMatterSearch/2021/NTuplizer/CMSSW_10_6_17_patch1/src/PPSFramework/working",
    'eospath': "/store/group/phys_exotica/PPS-Exo/Grid",
    'name': "PYTHIA8-SD-TOP-13TEV",
    'sample': "/PYTHIA8-SD-TOP-GEN/dmf-PYTHIA8-SD-TOP-MINIAOD-withpps-13TEV-c1a41892bad32b8e981acbdc0a984950/USER",
    'mode': "mc_private_analysis",
    'lumimask': "",
    'config': "/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/DarkMatterSearch/2021/NTuplizer/CMSSW_10_6_17_patch1/src/PPSFramework/Skimmer/test/RunMissingMassSearches.py",
    'parameters':("ppstagging=False", "physics=muon","mode=mc","trigger=False"),
    'input': (""),
    'output':("output.root"),
    'unitsperjob': 10,
    'site': "T2_CH_CERN",
})

print(json.dumps(data, indent=4))

with open("samples_crab.json", "w") as write_file:
    json.dump(data, write_file, indent = 4)

