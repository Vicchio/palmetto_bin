#!/usr/bin/env python
# 
# Stephen Patrick Vicchio 
# 2019-02-13
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 
# Populates the INCAR and subvasp.sh files for job submission 
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
#  INPUT: [file-template].ini  
# OUTPUT: INCAR and pbs submission files for running the job  
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import sys
import os
import argparse 
from shutil import copy

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

#TODO: add a flag so that I don't always have to take from 00-MOF 
TEMPLATE_DIR = '/common/curium/svicchi/zy-templates/00-MOF'
PBS_SUB_DIR  = '/common/curium/svicchi/zy-templates'


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

KEY_C6   = 'C6'
KEY_R0   = 'R0'
KEY_LIST = 'LIST_'

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# List of all functions

def hello_world():
	print('\nHello World\n')
	return 

def parsing_atoms(atom_list):
    """
    Function: assigns DFT2 parameters based on the atoms order
    Input: Atoms order
    Output: Dict of dicts with outer keys being atoms and inner keys as params
    """
    
    dict_atom = {}
    dict_atom[KEY_LIST] = atom_list
    for atom in atom_list.split():
        dict_atom[atom] = {}
        dict_atom[atom][KEY_C6] = dispersion_values(atom)[0]
        dict_atom[atom][KEY_R0] = dispersion_values(atom)[1] 	
        
    return dict_atom 

def string_generation_dis(dict_):
 
    C6_string = []
    R0_string = []
    
    for atom_in in dict_[KEY_LIST].split():
 #        print(dict_[atom_in][KEY_C6], type(dict_[atom_in][KEY_C6]))
        string_C6, status_C6 = filling_strings(str(dict_[atom_in][KEY_C6]),
                                               [KEY_C6])
        string_R0 = filling_strings(str(dict_[atom_in][KEY_R0]),
                                    [KEY_R0],status=status_C6)[0]
        
        print(string_C6,string_R0)
        
#        C6_string.append((str(dict_[atom_in][KEY_C6])))
#        R0_string.append((str(dict_[atom_in][KEY_R0])))

#        print(filling_strings(str(dict_[atom_in][KEY_C6]),[KEY_C6]))
           
    print(" ".join(C6_string))
    print(" ".join(R0_string))

        
    return 

def filling_strings(string, key_, status=False):
    string_out = None 
    if key_ == [KEY_C6] and status is False:
        if len(string.split('.')[0]) == 2:
            status = True 
            string_out = string
            print('I made it here!')
        elif len(string.split('.')[0]) == 1:
            status = False
            string_out = string
        else:
            raise ValueError('\n\n Issue with DFT2 Parameters\n')
    
#    if key_ == [KEY_R0]:
#        if status is False:
#            string_out = string
#        elif status is True: 
#            string_out = ' ' + string
#            
    return string_out, status

def populating_submission_file(name):
	

	return 

def creating_job_name_txt(name):

    with open(os.path.join(os.getcwd(), 'aa_' + str(name)), "w") as f:
        f.write('The following job is being run: ' + name)
        f.close
    return
 
def dispersion_values(atom):
    """
    The following values were taken from: 'Semiempirical GGA-Type Density 
    Functional Constructed with a Long-Range Dispersion Correction' by Grommes 
    et al. (2006). 

    Function: Returns the DFT2 parameters to include dispersion in calculation
    Input: atom string (i.e. C)
    Output: The C6 and R0 parameters for DFT2
    """
    
    dict_dis_C6 = {'H' : 0.140,
                   'He': 0.080,
                   'Li': 1.610,
                   'Be': 1.610,
                   'B' : 3.130,
                   'C' : 1.750,
                   'N' : 1.230,
                   'O' : 0.700,
                   'F' : 0.750,
                   'Ne': 0.630,
                   'Na': 5.710,
                   'Mg': 5.710,
                   'Al': 10.79,
                   'Si': 9.230,
                   'P' : 7.840,
                   'S' : 5.570,
                   'Cl': 5.070,
                   'Ar': 4.610,
                   'K' : 10.80,
                   'Ca': 10.80,
                   'Sc': 10.80,
                   'Ti': 10.80,
                   'V' : 10.80, 
                   'Cr': 10.80, 
                   'Mn': 10.80, 
                   'Fe': 10.80, 
                   'Co': 10.80, 
                   'Ni': 10.80,
                   'Cu': 10.80,
                   'Zn': 10.80,
                   'Zr': 24.67} 
	
    dict_dis_R0 = {'H' : 1.001,
                   'He': 1.012,
                   'Li': 0.825,
                   'Be': 1.408,
                   'B' : 1.485,
                   'C' : 1.452,
                   'N' : 1.397,
                   'O' : 1.342,
                   'F' : 1.287,
                   'Ne': 1.243,
                   'Na': 1.144,
                   'Mg': 1.364,
                   'Al': 1.639,
                   'Si': 1.716,
                   'P' : 1.705,
                   'S' : 1.683,
                   'Cl': 1.639,
                   'Ar': 1.595,
                   'K' : 1.485,
                   'Ca': 1.474,
                   'Sc': 1.562,
                   'Ti': 1.562,
                   'V' : 1.562,
                   'Cr': 1.562,
                   'Mn': 1.562,
                   'Fe': 1.562,
                   'Co': 1.562,
                   'Ni': 1.562,
                   'Cu': 1.562,
                   'Zn': 1.562,
                   'Zr': 1.639}  

    if atom not in dict_dis_C6.keys():
        raise ValueError('\n\nAtom Dispersion NOT listed!\n')
    else:
        C6_val = dict_dis_C6[atom]
        R0_val = dict_dis_R0[atom]

    return C6_val, R0_val


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Main code program

def main():
	# parsing the input arguments
    parser = argparse.ArgumentParser(description="""\nThis script is
                                     designed to fill premade template fills
                                     using .ini files to create INCAR and PBS 
                                     submission files.""")
    parser.add_argument('-i', action='store', dest='ini_file', 
                        help='.ini file to populate template')
    parser.add_argument('-l', action='store', dest='potcar_atoms_order')
    parser.add_argument('-n', action='store', dest='job_name',
                        help='type of job being run')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
   
    args = parser.parse_args()

	# organizing the arguments 	
    atom_dict = parsing_atoms(args.potcar_atoms_order)
    string_generation_dis(atom_dict)
	# identifying the necessary template files 
    creating_job_name_txt(args.job_name)
    copy(os.path.join(PBS_SUB_DIR, 'template_subvasp.sh'), 
         os.path.join(os.getcwd(), 'subvasp.sh-gen'))
    copy(os.path.join(TEMPLATE_DIR, 'INCAR.txt'), 
         os.path.join(os.getcwd(), 'INCAR-gen'))
	
	# modifying the template file 
    
    

    return 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if __name__ == '__main__':
	main()

