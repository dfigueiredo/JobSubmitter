#!/usr/bin/env python

#!interpreter [optional-arg]
# -*- coding: utf-8 -*-

""" Console for crab/condor jobs submission.
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

import os 

print("\nRunning Grid Tool Submission\n")

if "PYTHONPATH" in os.environ:
    pythonpath = os.getenv("PYTHONPATH")
    print("\t >> PYTHONPATH is defined as {}.\n".format(pythonpath))
else:
    print("\t >> Please, source the script to enable crab library\n\t\t >> i.e.: source /cvmfs/cms.cern.ch/common/crab-setup.sh\n")
    exit()

if "CMSSW_BASE" in os.environ:
    cmsswpath = os.getenv("CMSSW_BASE")
    print("\t >> CMSSW_BASE is defined as {}.\n".format(cmsswpath))
else:
    print("\t >> Please, source the cmsenv to enable the CMSSW version you would like to use before submit your crab jobs\n\t\t >> i.e.: [cd CMSSW_X_Y_Z/src] and cmsenv\n")
    exit()


from cmd import Cmd
from submitter import colors
from submitter import gridlibrary
from optparse import OptionParser

import CRABClient
from CRABClient.UserUtilities import config

def getOptions():

    """
    Parse and return the arguments provided by the user.
    """

    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-f", "--filename",
                  metavar="FILE", help="JSON mapping file", default='samples.json')
    parser.add_option("-p", "--parsing",
                  help="parsing: commands which can be passed from SHELL directly. [parsing: --p \"submit --file samples.json\"]")

    parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="make lots of noise [default]")

    (options, arguments) = parser.parse_args()
    return options

class MyPrompt(Cmd):
    prompt = 'crab_submission> '
    intro = "Type ? to list commands"
 
    def do_exit(self, inp):
        print("\n [submitter] Exiting...\n")
        return True
    
    def help_exit(self):
        print('[submitter] exit the application. Shorthand: x q Ctrl-D.')
 
    def do_submit(self, arg):

	arcmd = arg.split()
	filename = options.filename

	if ("--file" or "--f") in arg: 
                if len(arcmd)>1:
                        for i in arcmd[1:]:
                                filename=str(i)

		if os.path.exists(filename):
	        	json = gridlibrary.Parser(filename, options.verbose)
	        	json.prepareSubmission()
		
		else:
        	        print color.FAIL+color.BOLD+'\t[submitter] JSON file does not exist or wrong path! Please use the option --file filename.json or run the application again with the option --f filename.json'+color.ENDC+color.HEADER+color.ENDC

	else:
                json = gridlibrary.Parser(options.filename, options.verbose)
                json.prepareSubmission()
	
    def help_submit(self):
        print("\n\nUse the options --file filename.json\n\tEx: submit --file filename.json <press enter>\n\n")

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)
 
        print("Default: {}".format(inp))

    def emptyline(self):
        pass

    do_EOF = do_exit
    help_EOF = help_exit
 
if __name__ == '__main__':

    color = colors.Paint()
    options = getOptions()

    #config = config()

    if options.parsing:
	MyPrompt().onecmd(''.join(options.parsing))
    else:
        MyPrompt().cmdloop()

