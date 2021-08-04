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

from httplib import HTTPException
from multiprocessing import Process

color = colors.Paint()
NBLOCKS = 7 # number of keys per dataset block.
gridenable = False # enable submission for a specific CMS T2. Please, use it carefully and in contact with your T2 grid admin.
condor_server = "_CONDOR_SCHEDD_HOST=bigbird17.cern.ch _CONDOR_CREDD_HOST=bigbird17.cern.ch"

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
          print("\n"+color.FAIL+"[submitter:condor] The file {} is not valid.\nPlease, check it."+color.ENDC+"\n").format(json_file)
          exit()

        if "datasets" in self.data:
         for p in self.data["datasets"]:
          self.count_data = self.count_data + 1
          if "id" not in p:
            print("\n"+color.FAIL+"[submitter:condor] The key \"id\" must be defined in each dataset bracket.\nPlease, check it."+color.ENDC+"\n")
            exit()
          else:
            check_id = isinstance(p["id"], int)
            if not check_id:
             print("\n"+color.FAIL+"[submitter:condor] The key \"id\" must be integer. Id is defined as {}.\nPlease, check it."+color.ENDC+"\n").format(type(p["id"]))
             exit()
          for key in p:
           if "id" == key or\
              "enable" == key or\
              "inputfolder" == key or\
              "executable" == key or\
              "inputfiles" == key or\
              "parameters" == key or\
              "output" == key:
            self.count_key = self.count_key + 1
           else:
            print("\n"+color.FAIL+"[submitter:condor] {} is _not_ a valid key for the dataset id {}.\nPlease, check your JSON file."+color.ENDC+"\n").format(str(key), str(self.count_key))
            exit()
        else:
            print("\n"+color.FAIL+"[submitter:condor] JSON file is not correct.\nPlease, check it."+color.ENDC+"\n")
            exit()

        check = int(self.count_key)/int(self.count_data)
        if not (check==NBLOCKS):
            error_message = '\n'+color.FAIL+'[submitter:condor] Defined {} keys instead of a total of {} keys in your JSON file.\n'\
                            'In case you are sure the file has the exactly number of parameters you need, you should re-define NBLOCKS in the code accordinly.'\
                            '\nPlease, correct it instead.'+color.ENDC+'\n'
            print(error_message).format(check, NBLOCKS)
            exit()
 
        if verbose:
         print "\n[submitter:condor] Reading file...\n"
         print(color.BOLD + json.dumps(self.data, indent=4, sort_keys=True) + color.ENDC)
         print "\n"

    def submit(self, command):
        try:
         with open("job_condor_tmp.sub", "w") as fout:
          fout.write(command)
          fout.close()
          os.system(condor_server+" condor_submit job_condor_tmp.sub")
          os.system("rm job_condor_tmp.sub")
        except HTTPException as hte:
            print "Failed submitting task: %s" % (hte.headers)
        except ClientException as cle:
            print "Failed submitting task: %s" % (cle)

    def fromListToString(self,list_set, withComma):
     outStr=""
     unique_list = (list(list_set))
     counter = 0
     for x in unique_list:
      if withComma:
       if counter > 0:
        outStr += ", "+x
       else:
        outStr += x
      else:
        outStr += " "+x
      counter += 1
     return outStr

    def prepareSubmission(self):

     if "datasets" in self.data:
      for p in self.data["datasets"]:

       print "\n\t" + color.BOLD + "id: " + color.ENDC,
       print "\t" + color.OKGREEN + str(p["id"]) + color.ENDC

       print "\t" + color.BOLD + "enable: " + color.ENDC,
       print "\t" + color.OKGREEN + str(p["enable"]) + color.ENDC

       print "\t" + color.BOLD + "inputfolder: " + color.ENDC,
       print "\t" + color.OKGREEN + str(p["inputfolder"]) + color.ENDC
 
       print "\t" + color.BOLD + "executable: " + color.ENDC,
       print "\t" + color.OKGREEN + str(p["executable"]) + color.ENDC

       print "\t" + color.BOLD + "inputfiles: " + color.ENDC,
       print "\t" + color.OKGREEN + str(p["inputfiles"]) + color.ENDC

       print "\t" + color.BOLD + "parameters: " + color.ENDC,
       print "\t" + color.OKGREEN + str(p["parameters"]) + color.ENDC

       print "\t" + color.BOLD + "output: " + color.ENDC,
       print "\t" + color.OKGREEN + str(p["output"]) + color.ENDC

       par_executable = self.fromListToString(p["parameters"], False)
       par_input_files = self.fromListToString(p["inputfiles"], True)

       if isinstance(p["output"], unicode):
          if not os.path.exists(str(p["output"])):
           os.makedirs(str(p["output"]))
           print "\t" + color.BOLD + "Creating a new directory " + color.ENDC,
           print "\t" + color.OKBLUE + str(p["output"]) + color.ENDC
 
       else:
          print("\n"+color.FAIL+"[submitter:condor] Parameter output must be a string.\nPlease, check it."+color.ENDC+"\n")
          exit()

       # Condor commands
       command =  "initialdir\t\t\t= "+str(p["output"])+"\n"
       command += "executable\t\t\t= "+str(p["executable"])+"\n"
       command += "arguments\t\t\t= "+str(par_executable)+ "\n"
       #command += "transfer_input_files\t\t\t= "+str(par_input_files) + "\n"
       command += "output\t\t\t= execution.$(ClusterId).$(ProcId).out\n"
       command += "error\t\t\t= fail.$(ClusterId).$(ProcId).err\n"
       command += "log\t\t\t= status.$(ClusterId).$(ProcId).log\n"
       command += "getenv\t\t\t= True\n"

       ###########################
       # espresso     = 20 minutes
       # microcentury = 1 hour
       # longlunch    = 2 hours
       # workday      = 8 hours
       # tomorrow     = 1 day
       # testmatch    = 3 days
       # nextweek     = 1 week
       ##########################

       command += "+JobFlavour\t\t\t= \"workday\"\n"
       command += "requirements\t\t\t = (OpSysAndVer =?= \"CentOS7\")\n"

       if gridenable: 
        command += "Universe\t\t\t= grid\n"
        command += "Should_Transfer_Files\t\t\t = YES\n"
        command += "when_to_transfer_output\t\t\t = ON_EXIT_OR_EVICT\n"
        command += "x509userproxy\t\t\t = /tmp/x509up_u30993\n"
        command += "use_x509userproxy\t\t\t = true\n"
        command += "grid_resource\t\t\t= condor osgce2.hepgrid.uerj.br osgce2.hepgrid.uerj.br:9619\n"
        command += "+remote_jobuniverse\t\t\t= 5\n"
        command += "+remote_requirements\t\t\t= True\n"
        command += "+remote_ShouldTransferFiles\t\t\t= \"YES\"\n"
        command += "+remote_WhenToTransferOutput\t\t\t= \"ON_EXIT\"\n"
        command += "accounting_group_user\t\t\t= dmf\n"
        command += "accounting_group\t\t\t= group_uerj\n"
        command += "RequestCpus\t\t\t = 4\n"
        command += "+MaxRuntime\t\t\t = 7200\n"
        command += "max_transfer_input_mb\t\t\t = 2048\n"
        command += "max_transfer_output_mb\t\t\t = 2048\n"

       command += "queue filename matching files "+p["inputfolder"]+"*.root\n"

       if int(p["enable"]):
        self.submit(command)
       else:
        print "\t" + color.BOLD + color.HEADER + "-- Submittion not enabled --" + color.ENDC
       print("\n")
