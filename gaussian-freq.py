#!/usr/bin/env python
#
# Stephen Patrick Vicchio
# 2022-01-11
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# [gausian-xyz.py] Creates xyz file for the structure and identifies whether or
#                  not the structure is converged or not
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
#  INPUT: gaussian log file
# OUTPUT: gaussian xyz file representing the last step in the calculation
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   I M P O R T S


import os
import re
import ase
from ase.io.trajectory import Trajectory
import argparse
import numpy as np

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

class freq_reader(object):
    '''
    updates the frequency files so that they can be viewed correctly 
    '''
    def __init__(self,
                 dirname,  # the directory for the calculation
                 filename, # the filename for for calculation
                ):
        '''
        initializing the scipt
        '''
        
        # initializng all the variables
        self.dirname = dirname
        self.filename = filename
        
        # atomic number to element dict 
        self.atomic_number_2_element = {
            '1': 'H',
            '2': 'He',
            '3': 'Li',
            '4': 'Be',
            '5': 'B',
            '6': 'C',
            '7': 'N',
            '8': 'O',
            '9': 'F',
            '10': 'Ne',
            '11': 'Na',
            '12': 'Mg',
            '13': 'Al',
            '14': 'Si',
            '15': 'P',
            '16': 'S',
            '17': 'Cl',          
            '18': 'Ar',
            
        }
        
        self.element_2_atomic_number = {}
        for key, val in self.atomic_number_2_element.items():
            self.element_2_atomic_number[val] = key
        
        # generating the lines for the calculation
        with open(os.path.join(self.dirname, self.filename), 'r') as RAW_FILE:
            self.all_lines = RAW_FILE.readlines()
        RAW_FILE.close()


        
        # finding the converge status
        KEY_CONVERGE = ' -- Stationary point found.'
        re_search_converge = re.compile(KEY_CONVERGE)
        self.convergence_status = False
        
        # finding the frequency status
        KEY_FREQ = ' \#p freq'
        re_search_freq = re.compile(KEY_FREQ)
        self.freq_status = False
        
        # finding wether or not it's gaussian16 or not...
        KEY_G16 = 'This is part of the Gaussian\(R\) 16 program.'
        re_search_G16 = re.compile(KEY_G16)
        self.g16_status = False 
        
        for line in self.all_lines:
            if re_search_converge.search(line):
                self.convergence_status = True
            if re_search_G16.search(line):
                self.g16_status = True  
            if re_search_freq.search(line):
                self.freq_status = True 
        
        # if a g16, freq calculation... 
        if self.g16_status and self.freq_status:

            # finding the frequency status
            KEY_DIPOLE = ' Dipole orientation'
            re_search_dipole = re.compile(KEY_DIPOLE)
            self.dipole_status = False
            
            KEY_DIPOLE_STOP = '   zzz'
            re_search_dipole_stop = re.compile(KEY_DIPOLE_STOP)
            
            # finding which lines to delete
            for line_index in range(0,len(self.all_lines)):
                if re_search_dipole.search(self.all_lines[line_index]):
                    self.dipole_status = True
                    index_remove_start = line_index
                elif self.dipole_status and re_search_dipole_stop.search(self.all_lines[line_index]): 
                    index_remove_end = line_index + 1
                    self.dipole_status = False
                    
                
            # deleting the lines that cause problems
            del self.all_lines[index_remove_start:index_remove_end]
            
            # renaming the files to have a backup
            os.rename(os.path.join(self.dirname, self.filename), os.path.join(self.dirname, self.filename + '.archive'))
            
            # writing the new log file
            with open(os.path.join(self.dirname, self.filename), 'w') as RAW_FILE:
                for line in self.all_lines:
                    RAW_FILE.write(line)
            RAW_FILE.close()



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# M A I N   F U N C T I O N

def main():
    # Parsing the command line arguments
    parser = argparse.ArgumentParser(description="""\n
            This script removes the section that doesnt allow G16 freq log files to be viewed\n
            in GaussView5.
            \n""")
    parser.add_argument('-log', action='store', dest='LOG', default=None,
             help='freq log file')
   

    args = parser.parse_args()
    
    
    
    gaussian_object = freq_reader(dirname  = os.getcwd(),
                                  filename = args.LOG,
                                 )





# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T

if __name__ == '__main__':
        main()

