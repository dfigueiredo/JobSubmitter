import json

# Options:
# id (int): identify the key we are submiting.
# enable (bool): to activate/deactivate the crab jobs submission for a given dataset

data = {}
data['datasets'] = []

data['datasets'].append({
    'id': 0,
    'enable': 1,
    'inputfolder': "/eos/cms/store/group/phys_exotica/PPS-Exo/crab_BTagCSV_B_2021-02-03_UTC11-46-13_2021-02-03_UTC11-46-13/BTagCSV/crab_BTagCSV_B_2021-02-03_UTC11-46-13/210203_104633/0000/",
    'executable': "./MissingMassNtupleAnalyzer",
    'inputfiles': ("../proton_reco_rphorizontal_Electron_era_B_xa_120.txt","../proton_reco_rphorizontal_Electron_era_B_xa_130.txt"),
    'parameters':("--f $(filename)","--era B","--mode Bjets","--xa 0","--datatype Data","--jobid $(ProcId)","--none"),
    'output': ("BJets_data_era_B/")
})

print(json.dumps(data, indent=4))

with open("samples_condor.json", "w") as write_file:
    json.dump(data, write_file, indent = 4)

