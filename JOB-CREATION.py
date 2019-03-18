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
INCAR   = 'INCAR'

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
    parser.add_argument('-i', action='store', dest='START_DIR', default=STAGE1, 
                        help='the name of the first directory to start job from')
    parser.add_argument('-s', action='store', dest='COUNT_CONT', default=int(5),
                        type=int, help='number of stages to create')
    args = parser.parse_args()
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #       
# Determining the status of the current run 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  

    try: 
        if os.path.isdir(os.path.join(DIR_, args.START_DIR)) is True: 
            stage1_dir = os.path.join(DIR_, args.START_DIR)
            status_POTCAR  = os.path.isfile(os.path.join(stage1_dir, POTCAR))
            status_KPOINTS = os.path.isfile(os.path.join(stage1_dir, KPOINTS))
            status_WAVECAR = os.path.isfile(os.path.join(stage1_dir, WAVECAR))
            status_CONTCAR = os.path.isfile(os.path.join(stage1_dir, CONTCAR)) 
            status_INCAR   = os.path.isfile(os.path.join(stage1_dir, INCAR)) 
            if status_POTCAR is False or status_KPOINTS is False or status_WAVECAR is False or status_CONTCAR is False or status_INCAR is False: 
                sys.stderr.write(FAIL)
                sys.stderr.write("\nOne of the big four files is missing from " + str(args.START_DIR).strip + "!\n")
                sys.stderr.write(ENDC+"\n")
                sys.exit()
            else: 
                stage1_POTCAR  = os.path.join(stage1_dir, POTCAR)
                stage1_KPOINTS = os.path.join(stage1_dir, KPOINTS)
                stage1_WAVECAR = os.path.join(stage1_dir, WAVECAR)
                stage1_CONTCAR = os.path.join(stage1_dir, CONTCAR)
                stage1_INCAR   = os.path.join(stage1_dir, INCAR)

    except IOError:
        sys.stderr.write(FAIL)
        sys.stderr.write("\nThe 00-1st-stage directory doesn't exist.\n")
        sys.stderr.write(ENDC+"\n")
        sys.exit()
        
    if args.START_DIR is STAGE1:
        dir_start = 0
    else: 
        dir_start = int(args.START_DIR.split('-')[0])
    
    print(dir_start)

 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #       
# Starting to create the new-directories for future runs
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
        
    for i in range(dir_start+2, args.COUNT_CONT+2):
        print(str(i).zfill(2))
    
        
        
        
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T 
    
if __name__ == '__main__':
        main()
