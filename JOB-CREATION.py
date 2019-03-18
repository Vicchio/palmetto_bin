#!/usr/bin/env python
#
# Stephen Patrick Vicchio
# 2019-03-18
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
# [JOB-CREATION.py] Creates the necessary directories and files to start new 
# jobs for MOF calculations in VASP 
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
#  INPUT: POSCAR from VASP 
# OUTPUT: Directories with correct files located  
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# L I S T   O F   I M P O R T S 

import argparse
import os 
import sys 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   P A R A M E T E R S 

FAIL = '\033[91m'
ENDC = '\033[0m'

DIR_ = os.getcwd()
STAGE1  = '00-1st-stage'
POTCAR  = 'POTCAR'
KPOINTS = 'KPOINTS'
CONTCAR = 'CONTCAR'
WAVECAR = 'WAVECAR' 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   F U N C T I O N 

def main():
    # Parsing the command line arguments
    parser = argparse.ArgumentParser(description="""\n This script requires 
                                     information on the first directory for a
                                     particular run. The first directory must
                                     contain the KPOINTS, WAVECAR, INCAR, and
                                     POTCAR to continue VASP calculation runs.
                                     \n""")
#    parser.add_argument('-i', action='store', dest='POSCAR_FILE', default=None,
#                        help='POSCAR file to read')
#    parser.add_argument('-p', action='store', dest='POTCAR_FILE', default=None,
#                        help='POTCAR file to read')
    args = parser.parse_args()
    
#    try: 
#        status_stage1_dir = os.path.isdir(os.path.join(DIR_, STAGE1))
#    except IOError: 
#        sys.stderr.write(FAIL)
#        sys.stderr.write("\nThe 00-1st-stage directory doesn't exist.\n")
#        sys.stderr.write(ENDC+"\n")
#        sys.exit()
    
    if os.path.isdir(os.path.join(DIR_, STAGE1)) is True: 
        stage1_dir = os.path.join(DIR_, STAGE1)
        status_POTCAR  = os.path.isfile(os.path.join(stage1_dir, POTCAR))
        status_KPOINTS = os.path.isfile(os.path.join(stage1_dir, KPOINTS))
        status_WAVECAR = os.path.isfile(os.path.join(stage1_dir, WAVECAR))
        status_CONTCAR = os.path.isfile(os.path.join(stage1_dir, CONTCAR))
        
        
        print(status_POTCAR, status_KPOINTS, status_WAVECAR, status_CONTCAR)
        
    else: 
        sys.stderr.write(FAIL)
        sys.stderr.write("\nThe 00-1st-stage directory doesn't exist.\n")
        sys.stderr.write(ENDC+"\n")
        sys.exit() 
    

 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #       
# READING THE POTCAR AND POSCAR FILES 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
        
        
        
        
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T 
    
if __name__ == '__main__':
        main()
