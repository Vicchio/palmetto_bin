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
import re 
from shutil import copy2



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   P A R A M E T E R S 

FAIL = '\033[91m'
ENDC = '\033[0m'

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# List of Directories

DIR_ = os.getcwd()
TEMPLATE_DIR = os.path.join(DIR_, 'JOB-CREATION-TEMPLATES')

STAGE1    = '00-1st-stage'
POTCAR    = 'POTCAR'
KPOINTS   = 'KPOINTS'
CONTCAR   = 'CONTCAR'
WAVECAR   = 'WAVECAR' 
INCAR     = 'INCAR'
INCAR_NEW = 'INCAR.temp'
POSCAR    = 'POSCAR'
POSCAR_N  = 'PSOCAR.temp'


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
                '10': '11th'}

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   F U N C T I O N 

def change_incar_file(dir_work, ISTART, NSW):
    """
    Modified the INCAR file to contain updated parameters
    
    [INPUTS]
    (1) dir_work - the dir that will contain the new INCAR file 
    (2) ISTART   - information on whether or not to use the WAVECAR or not
    (3) NSW      - the number of ionic steps to be completed in the calculation 
    
    [OUTPUTS]
    (1) the modified INCAR file in the dir_work directory 
    
    """
    
    incar_file = os.path.join(dir_work, INCAR)
        
    try: 
        incar = open(incar_file,"r")
    except IOError:
        sys.stderr.write(FAIL)
        sys.stderr.write("\nThere was a problem reading the INCAR file.\n")
        sys.stderr.write(ENDC+"\n")
        sys.exit(1)
    
    re_nsw = re.compile('NSW     =')
    re_ist = re.compile('ISTART  =')
    
    with open(os.path.join(dir_work, INCAR_NEW), 'w') as new_incar: 
        for line in incar.readlines():
            new_line = line
          
            if re_ist.search(line):
                split_line = line.split()
                new_line = str(split_line[0].rjust(6) + split_line[1].rjust(3) + str(ISTART).rjust(2) + split_line[3].rjust(11) + line.split('#')[1].rjust(40))
            if re_nsw.search(line):      
                split_line = line.split()
                new_line = str(split_line[0].rjust(3) + split_line[1].rjust(6) + str(NSW).rjust(3) + split_line[3].rjust(10) + line.split('#')[1].rjust(40))   
            new_incar.write(new_line)
    new_incar.close()
    os.remove(os.path.join(dir_work, INCAR))
    os.rename(os.path.join(dir_work, INCAR_NEW), os.path.join(dir_work, INCAR))    
            
    return 

def delete_poscar_velocity(dir_work):
    
    poscar_file = os.path.join(dir_work, POSCAR)
    
    print('I entered the function')
    
    try:
        poscar = open(poscar_file, 'r')
    except IOError:
        sys.stderr.write(FAIL)
        sys.stderr.write("\nThere was a problem reading the POSCAR file.\n")
        sys.stderr.write(ENDC+"\n")
        sys.exit(1)
     
    re_vel = re.compile('0.00000000E+00')
        
    with open(os.path.join(dir_work, POSCAR_N), 'w') as new_poscar:
        print('I am looking at the file!')
        for line in poscar.readlines():
            print(line)
            if re_vel.search(line): 
                print(line)
            else:
                new_poscar.write(line)
    new_poscar.close()
    os.remove(os.path.join(dir_work, POSCAR))
    os.rename(os.path.join(dir_work, POSCAR_N), os.path.join(dir_work, POSCAR))    
        
    return      
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# M A I N   P R O G R A M  

def main():
    # Parsing the command line arguments
    parser = argparse.ArgumentParser(description="""\n This script requires 
                                     information on the first directory for a
                                     particular run. The first directory must
                                     contain the KPOINTS, WAVECAR, INCAR, and
                                     POTCAR to continue VASP calculation runs.
                                     \n""")
    parser.add_argument('-s', action='store', dest='START_DIR', default=STAGE1, 
                        help='the name of the first directory to start job from')
    parser.add_argument('-c', action='store', dest='COUNT_CONT', default=int(4),
                        type=int, help='number of stages to create')
    parser.add_argument('-n', action='store', dest='NSW_COUNT', default=int(10),
                        type=int, help='number of NSW to take during each stage')
    parser.add_argument('-i', action='store', dest='ISTART', default=int(2), 
                        type=int, help='0: new WAVECAR, 2: old WAVECAR')
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
                sys.stderr.write("\nOne of the big four files is missing from " + str(args.START_DIR).strip() + "!\n")
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
     
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #       
# Starting to create the new-directories for future runs
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
        
    for i in range(dir_start+1, args.COUNT_CONT+2): 
        folder_ID = str(i).zfill(2) + '-' + JOB_COUNT_DICT[str(i).zfill(2)] + '-stage'
        dir_ID = os.path.join(DIR_, folder_ID)
        
        # Creates the new directory to continue job from previous run 
        os.mkdir(dir_ID)
        copy2(stage1_POTCAR, dir_ID)
        copy2(stage1_KPOINTS, dir_ID)  
        copy2(stage1_INCAR, dir_ID)
        
        if i == dir_start+1: 
            copy2(stage1_CONTCAR, dir_ID)
            os.rename(os.path.join(dir_ID, CONTCAR), os.path.join(dir_ID, CONTCAR + '-' + JOB_COUNT_DICT[str(i).zfill(2)] + '-stage'))
            copy2(stage1_CONTCAR, dir_ID)
            os.rename(os.path.join(dir_ID, CONTCAR), os.path.join(dir_ID, POSCAR))
            delete_poscar_velocity(dir_ID)
            
#            copy2(stage1_WAVECAR, dir_ID)

        # modifies in the INCAR file to contain the updated parameters 
        change_incar_file(dir_ID, ISTART=args.ISTART, NSW=args.NSW_COUNT)
        
        
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T 
    
if __name__ == '__main__':
        main()
