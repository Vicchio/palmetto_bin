#!/usr/bin/env python
#
# Stephen Patrick Vicchio
# 2021-09-07
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# [JOB-CREATION.py] Creates the new submission files for a Gaussian restart
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
#  INPUT:
# OUTPUT:
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   I M P O R T S

import argparse
import os
import sys
import re
from shutil import copy2
import subprocess

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   P A R A M E T E R S

FAIL = '\033[91m'
ENDC = '\033[0m'

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# List of Directories

DIR_ = os.getcwd()

JOB_COUNT_DICT={'00': '1st',
                '01': '2nd',
                '02': '3rd',
                '03': '4th',
                '04': '5th',
                '05': '6th',
                '06': '7th',
                '07': '8th',
                '08': '9th',
                '09': '10th',
                '10': '11th',
                '11': '12th',
                '12': '13th',
                '13': '14th',
                '14': '15th',
                '15': '16th',
                '16': '17th',
                '17': '18th',
                '18': '19th',
                '19': '20th'}

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   F U N C T I O N



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   C L A S S E S 


class log_finder(object):
    def __init__(self, root_dir):
        '''
        Initalizing the function to find the files
        '''
        self.root_dir = root_dir
        
        self.list_files = os.listdir(self.root_dir)
        
        for file in self.list_files:
            if file.endswith('chk'):
                self.chk_filename = file
            elif file.endswith('log'):
               self.log_filename = file
            elif file.endswith('gjf'):
                self.gjf_filename = file
            elif file.endswith('sh'):
                self.sh_filename = file
            else:
                pass
        
        
        with open(os.path.join(self.root_dir,self.log_filename), 'r') as RAW_FILE:
            all_lines = RAW_FILE.readlines()
        RAW_FILE.close()
        
        self.all_lines = all_lines

        return

    def convergence_check(self):
        '''
        Checking that all the calculations converged correctly
        '''
        
        KEY_CONVERGE = ' -- Stationary point found.'
        re_search_converge = re.compile(KEY_CONVERGE)
        
        self.convergence_status = False
        for line in self.all_lines:
            if re_search_converge.search(line):
                self.convergence_status = True
               
        return 

    def generate_restart(self):
        '''
        Generate the restart file for the current calculation
        '''

        if self.convergence_status is True:
            print('\n The calculation converged! What are you doing, Stephen? \n')
        else:
            if os.path.basename(self.root_dir) == '00-opt':
                # finding the new dir name
                dir_num_old = os.path.basename(os.path.dirname(self.root_dir))
                dir_num_new = str(int(dir_num_old.split('-')[0]) + 1 ).zfill(2)
                dir_name_new = str(dir_num_new) + '-' + JOB_COUNT_DICT[dir_num_new] + '-stage'
               
                # Finding the calculation job command 
                KEY_JOBINFO = '#p opt='
                re_search_JOBINFO = re.compile(KEY_JOBINFO)
                
                for line in self.all_lines:
                    if re_search_JOBINFO.search(line):
                        print(line)

                # generate dir to copy over files
                dir_loc_new = os.path.join((os.path.dirname(os.path.dirname(self.root_dir))),dir_name_new)

                # shutil 


        return 


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# M A I N   F U N C T I O N

def main():
    # Parsing the command line arguments
    parser = argparse.ArgumentParser(description="""\n
            This script generates a restart file for a Gaussian calculations.                         
            \n""")
    parser.add_argument('-log', action='store', dest='LOG', default=None,
             help='unconverged log file')
    args = parser.parse_args()
    
    restart_function =  log_finder(os.getcwd())
    restart_function.convergence_check()
    restart_function.generate_restart()
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T

if __name__ == '__main__':
        main()

