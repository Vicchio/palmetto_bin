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

class log_reader(object):
    '''
    Generates the phase for ab initio thermodynamic analysis 
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
            '40': 'Zr',
            '26': 'Fe',
        }
        
        self.element_2_atomic_number = {}
        for key, val in self.atomic_number_2_element.items():
            self.element_2_atomic_number[val] = key
        
        # generating the lines for the calculation
        with open(os.path.join(self.dirname, self.filename), 'r') as RAW_FILE:
            self.all_lines = RAW_FILE.readlines()
        RAW_FILE.close()

        # determining the type of calculation
# ----------------------------------------------------------------------------
# TODO: figure out a way to determine what type of calculation is being 
#       submitted here for analysis
# ----------------------------------------------------------------------------

        # finding the converge status
        KEY_CONVERGE = ' -- Stationary point found.'
        re_search_converge = re.compile(KEY_CONVERGE)
        self.convergence_status = False
        
        # finding wether or not it's gaussian16 or not...
        KEY_G16 = 'This is part of the Gaussian\(R\) 16 program.'
        re_search_G16 = re.compile(KEY_G16)
        self.g16_status = False 
        
        for line in self.all_lines:
            if re_search_converge.search(line):
                self.convergence_status = True
            if re_search_G16.search(line):
                self.g16_status = True  
                
        # determining key parameters here
        if self.convergence_status and self.g16_status is False:
            # reading final structure
            self.traj = ase.io.read(os.path.join(self.dirname, self.filename),index=0,format='gaussian-out')
            self.positions   = self.traj.get_positions()
            self.atomic_nums = self.traj.get_atomic_numbers() 

        else:
            
            # setting up search statements
            KEY_INPUT = 'Input orientation'
            KEY_DISTANCE = 'Distance matrix'
            re_INPUT = re.compile(KEY_INPUT)
            re_DIS   = re.compile(KEY_DISTANCE)
            
            # finding the coordinates
            coord_search = False
            count = 0 
            for line in self.all_lines:            
                if re_INPUT.search(line):
                    coord_search = True 
                    count += 1
#                     write_lines.append(str(len(self.atomic_nums)).rjust(2) + '\n' + '           i='+ str(count).zfill(3) + '\n') 
                    write_last_lines = []
                    self.atomic_nums = []
                    list_coords = []

                elif re_DIS.search(line):
                    coord_search = False

                if coord_search:
                    if len(line.split()) == 6 and not line.split()[0] == 'Number':
                        atom_type = str(self.atomic_number_2_element[str(line.split()[1])]).rjust(3)
                        self.atomic_nums.append(self.element_2_atomic_number[atom_type.strip()])
                        x_coord  = line.split()[3]
                        y_coord  = line.split()[4]
                        z_coord  = line.split()[5]
                        list_coords.append([x_coord, y_coord, z_coord])
         
            self.positions = list_coords
                       
        
    def optimized_structure(self):
        '''
        generating the optimized structure
        '''
        
        # finding the lines
        write_lines = []
        write_lines.append(str(len(self.atomic_nums)).rjust(4) + '\n\n')    
        for index in range(0, len(self.atomic_nums)):
            atom_type = str(self.atomic_number_2_element[str(self.atomic_nums[index])]).rjust(3)
            x_coord  = str(self.positions[index][0]).rjust(21)
            y_coord  = str(self.positions[index][1]).rjust(21)
            z_coord  = str(self.positions[index][2]).rjust(21)
            write_lines.append(atom_type + x_coord + y_coord + z_coord + '\n')
        
        # determining the extension
        if self.convergence_status:
            extension = '_final_converged.xyz'
        else:
            extension = '_final_unconverged.xyz'
        
        # writing the file
        with open(os.path.join(self.dirname, self.filename.strip('.log') + extension), 'w') as RAW_FILE:
            for line in write_lines:
                RAW_FILE.writelines(line)
        RAW_FILE.close()
        
        return 
        
        
    def trajectory(self):
        '''
        generating the trajectory for the optimization
        '''
        write_lines = []
        
        # setting up search statements
        KEY_INPUT = 'Input orientation'
        KEY_DISTANCE = 'Distance matrix'
        re_INPUT = re.compile(KEY_INPUT)
        re_DIS   = re.compile(KEY_DISTANCE)
        
        # finding the coordinates
        coord_search = False
        count = 0 
        for line in self.all_lines:            
            if re_INPUT.search(line):
                coord_search = True 
                count += 1
                write_lines.append(str(len(self.atomic_nums)).rjust(2) + '\n' + '           i='+ str(count).zfill(3) + '\n') 
            elif re_DIS.search(line):
                coord_search = False
            
            if coord_search:
                if len(line.split()) == 6 and not line.split()[0] == 'Number':
                    atom_type = str(self.atomic_number_2_element[str(line.split()[1])]).rjust(3)
                    x_coord  = str(line.split()[3]).rjust(21)
                    y_coord  = str(line.split()[4]).rjust(21)
                    z_coord  = str(line.split()[5]).rjust(21)
                    write_lines.append(atom_type + x_coord + y_coord + z_coord + '\n')
            
        # determining the extension
        if self.convergence_status:
            extension = '_traj_converged.xyz'
        else:
            extension = '_traj_unconverged.xyz'
        
        # writing the file
        with open(os.path.join(self.dirname, self.filename.strip('.log') + extension), 'w') as RAW_FILE:
            for line in write_lines:
                RAW_FILE.writelines(line)
        RAW_FILE.close()
        
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
    
    
    
    gaussian_object = log_reader(dirname  = os.getcwd(),
                                 filename = args.LOG,
                                )
    gaussian_object.optimized_structure()
    gaussian_object.trajectory()





# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T

if __name__ == '__main__':
        main()

