#!/usr/bin/env python

#!interpreter [optional-arg]
# -*- coding: utf-8 -*-

""" Module used to submit crab jobs on grid.
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""
__author__ = "Diego Figueiredo"
__contact__ = "dmf@cern.ch"
__copyright__ = "Copyright 2021, INFN-Pisa"
__credits__ = ["Diego Figueiredo"]
__date__ = "2021/04/05"
__deprecated__ = False
__email__ =  "dmf@cern.ch"
__license__ = "GPLv3"
__maintainer__ = "developer"
__status__ = "Validation"
__version__ = "0.0.1"

import re
import json
from xml.dom import minidom
from submitter import colors
import numpy as numpy
import sys
import time
import os
import getpass

from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from CRABClient.UserUtilities import config
from httplib import HTTPException
from multiprocessing import Process

color = colors.Paint()
NBLOCKS = 14 # number of keys per dataset block.
NJOBS = 8000 # fixed number of jobs for mc_private_production mode.

class Parser():

    def __init__(self, filename, verbose):

        # Count number of JSON inputs (datasets)
        self.count_data = 0
        self.count_key = 0
        self.parameters = []        
 
        # parse a JSON file by name
        with open(filename) as json_file:
         try:
          self.data = json.load(json_file)
         except ValueError as err:
          print("\n"+color.FAIL+"[submitter:crab] The file {} is not valid.\nPlease, check it."+color.ENDC+"\n").format(json_file)
          exit()

        if "datasets" in self.data:
         for p in self.data["datasets"]:
          self.count_data = self.count_data + 1
          if "id" not in p:
            print("\n"+color.FAIL+"[submitter:crab] The key \"id\" must be defined in each dataset bracket.\nPlease, check it."+color.ENDC+"\n")
            exit()
          else:
            check_id = isinstance(p["id"], int)
            if not check_id:
             print("\n"+color.FAIL+"[submitter:crab] The key \"id\" must be integer. Id is defined as {}.\nPlease, check it."+color.ENDC+"\n").format(type(p["id"]))
             exit()
          for key in p:
           if "id" == key or\
              "enable" == key or\
              "localpath" == key or\
              "eospath" == key or\
              "name" == key or\
              "sample" == key or\
              "mode" == key or\
              "lumimask" == key or\
              "config" == key or\
              "parameters" == key or\
              "input" == key or\
              "output" == key or\
              "unitsperjob" == key or\
              "site" == key:
            self.count_key = self.count_key + 1
           else:
            print("\n"+color.FAIL+"[submitter:crab] {} is _not_ a valid key for the dataset id {}.\nPlease, check your JSON file."+color.ENDC+"\n").format(str(key), str(self.count_key))
            exit()
        else:
            print("\n"+color.FAIL+"[submitter:crab] JSON file is not correct.\nPlease, check it."+color.ENDC+"\n")
            exit()

        check = int(self.count_key)/int(self.count_data)
        if not (check==NBLOCKS):
            error_message = '\n'+color.FAIL+'[submitter:crab] Defined {} keys instead of a total of {} keys in your JSON file.\n'\
                            'In case you are sure the file has the exactly number of parameters you need, you should re-define NBLOCKS in the code accordinly.'\
                            '\nPlease, correct it instead.'+color.ENDC+'\n'
            print(error_message).format(check, NBLOCKS)
            exit()
 
        if verbose:
         print "\n[submitter:crab] Reading file...\n"
         print(color.BOLD + json.dumps(self.data, indent=4, sort_keys=True) + color.ENDC)
         print "\n"

    def is_empty_or_blank(self,msg):
        """ This function checks if given string is empty
        or contain only shite spaces"""
        return re.search("^\s*$", msg)


    def submit(self, config):
        try:
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print "Failed submitting task: %s" % (hte.headers)
        except ClientException as cle:
            print "Failed submitting task: %s" % (cle)
 
    def prepareSubmission(self):

     if "datasets" in self.data:
      for p in self.data["datasets"]:

       self.config=config()

       timestr = time.strftime("%Y-%m-%d_UTC%H-%M-%S")

       print "\n\t" + color.BOLD + "id: " + color.ENDC,
       print "\t" + color.OKGREEN + str(p["id"]) + color.ENDC

       print "\t" + color.BOLD + "enable: " + color.ENDC,
       print "\t" + color.OKGREEN + str(p["enable"]) + color.ENDC

       print "\t" + color.BOLD + "localpath: " + color.ENDC,
       print "\t" + color.OKGREEN + str(p["localpath"]) + color.ENDC
 
       print "\t" + color.BOLD + "eospath: " + color.ENDC,
       print "\t" + color.OKGREEN + str(p["eospath"]) + color.ENDC

       print "\t" + color.BOLD + "name: " + color.ENDC,
       print "\t" + color.OKGREEN + str(p["name"]) + color.ENDC

       print "\t" + color.BOLD + "sample: " + color.ENDC,
       print "\t" + color.OKGREEN + str(p["sample"]) + color.ENDC

       print "\t" + color.BOLD + "mode: " + color.ENDC,
       print "\t" + color.OKGREEN + str(p["mode"]) + color.ENDC

       print "\t" + color.BOLD + "lumimask: " + color.ENDC,
       print "\t" + color.OKGREEN + str(p["lumimask"]) + color.ENDC

       print "\t" + color.BOLD + "config: " + color.ENDC,
       print "\t" + color.OKGREEN + str(p["config"]) + color.ENDC

       print "\t" + color.BOLD + "parameters: " + color.ENDC,
       print "\t" + color.OKGREEN + str(p["parameters"]) + color.ENDC

       print "\t" + color.BOLD + "input: " + color.ENDC,
       print "\t" + color.OKGREEN + str(p["input"]) + color.ENDC

       print "\t" + color.BOLD + "output: " + color.ENDC,
       print "\t" + color.OKGREEN + str(p["output"]) + color.ENDC

       print "\t" + color.BOLD + "unitsperjob: " + color.ENDC,
       print "\t" + color.OKGREEN + str(p["unitsperjob"]) + color.ENDC

       print "\t" + color.BOLD + "site: " + color.ENDC,
       print "\t" + color.OKGREEN + str(p["site"]) + color.ENDC

       if not int(p["enable"]):
        print "\t" + color.BOLD + color.HEADER + "-- Submittion not enabled --" + color.ENDC
        continue

       tagname = 'crab_%s_%s' % (getpass.getuser(), timestr)
       localpath = '%s/%s/%s' % (p["localpath"], str(p["name"]), tagname)
       eospath = '%s/%s/%s' % (p["eospath"], str(p["name"]), tagname)

       if (isinstance(p["parameters"], list)) and not any([self.is_empty_or_blank(elem) for elem in p["parameters"]]):
         par_ = p["parameters"]
         self.config.JobType.pyCfgParams = []
         for i in range(len(par_)):
          self.config.JobType.pyCfgParams.append(str(par_[i]))
       else:
          if str(p["parameters"]):
           self.config.JobType.pyCfgParams = [str(p["parameters"])]

       if (isinstance(p["input"], list)) and not any([self.is_empty_or_blank(elem) for elem in p["input"]]):
         input_ = p["input"]
         self.config.JobType.inputFiles = []
         for i in range(len(input_)):
          self.config.JobType.inputFiles.append(str(input_[i]))
       else:
          if str(p["input"]): 
           self.config.JobType.inputFiles = [str(p["input"])]

       if (isinstance(p["output"], list)) and not any([self.is_empty_or_blank(elem) for elem in p["output"]]):
         out_ = p["output"]
         self.config.JobType.outputFiles = []
         for i in range(len(out_)):
          self.config.JobType.outputFiles.append(str(out_[i]))
       else:
         if str(p["output"]):
          self.config.JobType.outputFiles = [str(p["output"])]

       self.config.JobType.psetName = p["config"]
       self.config.Data.outLFNDirBase = eospath
       self.config.General.transferOutputs = True
       self.config.General.requestName = tagname
       self.config.General.workArea = localpath
       self.config.Site.storageSite = p["site"]

       # Crab parameters for each submission case
       if p["mode"] == "data_analysis":
        self.config.JobType.pluginName = 'Analysis'
        self.config.Data.inputDataset = str(p["sample"])
        self.config.Data.inputDBS = 'global'
        self.config.Data.splitting = 'LumiBased'
        self.config.Data.unitsPerJob = 20
        self.config.Data.publication = False
        self.config.Data.lumiMask = str(p["lumimask"])
        self.config.General.transferLogs = True
       elif p["mode"] == "mc_analysis":
        self.config.JobType.pluginName = 'Analysis'
        self.config.Data.inputDataset = str(p["sample"])
        self.config.Data.inputDBS = 'global'
        self.config.Data.splitting = 'FileBased'
        self.config.Data.unitsPerJob = 20
        self.config.Data.publication = False
        self.config.Data.lumiMask = str(p["lumimask"])
        self.config.General.transferLogs = True
       elif p["mode"] == "mc_private_analysis":
        self.config.JobType.pluginName = 'Analysis'
        self.config.Data.inputDataset = str(p["sample"])
        self.config.Data.inputDBS = 'phys03'
        self.config.Data.splitting = 'FileBased'
        self.config.Data.unitsPerJob = 20
        self.config.Data.publication = False
        self.config.General.transferLogs = True
       elif p["mode"] == "mc_private_hadron_production":
        self.config.JobType.pluginName = 'PrivateMC'
        self.config.Data.outputPrimaryDataset = str(p["name"])
        self.config.Data.inputDBS = 'phys03'
        self.config.Data.splitting = 'EventBased'
        self.config.Data.unitsPerJob = p["unitsperjob"]
        self.config.Data.totalUnits = NJOBS * self.config.Data.unitsPerJob
        self.config.Data.publication = True
        self.config.General.transferLogs = False
       elif p["mode"] == "mc_private_hadron_lhe_production":
        # https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3AdvancedTopic
        # https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3AdvancedTutorial#Exercise_5_LHE
        try:
         LHEEvents = input("\n\t" + color.BOLD + "Please, insert the number of the events into the LHE file (int) and type <enter>: " + color.ENDC)
         print("\tLHE number of events: " + str(LHEEvents) + "\n")
        except:
         print("\t" + color.FAIL + "Wrong type. Restart this tool."+color.ENDC+"\n\n") 
         exit()
        if not (isinstance(LHEEvents, int)):
         print("\t" + color.FAIL + "Wrong type. Restart this tool."+color.ENDC+"\n\n") 
         exit()
        nsplit = int(p["unitsperjob"])
        if LHEEvents <= nsplit:
         nsplit = int(0.1*LHEEvents)
        self.config.JobType.pluginName = 'PrivateMC'
        self.config.JobType.generator = 'lhe'
        self.config.Data.outputPrimaryDataset = str(p["name"])
        self.config.Data.inputDBS = 'phys03'
        self.config.Data.splitting = 'EventBased'
        self.config.Data.unitsPerJob = nsplit
        self.config.Data.totalUnits = int(LHEEvents)
        self.config.Data.publication = True
        self.config.General.transferLogs = False
        self.config.Site.whitelist = ["T2_CH_CERN"] 
       elif p["mode"] == "mc_private_production":
        self.config.Data.inputDataset = str(p["sample"])
        self.config.JobType.pluginName = 'Analysis'
        self.config.Data.outputDatasetTag = str(p["name"])
        self.config.Data.inputDBS = 'phys03'
        self.config.Data.splitting = 'FileBased'
        self.config.Data.unitsPerJob = p["unitsperjob"]
        self.config.Data.publication = True
        self.config.General.transferLogs = False
       else:
        print("\n"+color.WARNING+"[submitter:crab] mode {} is not defined.\nJobs have not been configured for the task id {}."+color.ENDC+"\n").format(p["mode"], p["id"])
        continue

       if int(p["enable"]):
        p = Process(target=self.submit, args=(self.config,))
        p.start()
        p.join()
       else:
        print "\t" + color.BOLD + color.HEADER + "-- Submittion not enabled --" + color.ENDC

       print("\n")
