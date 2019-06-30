#!/usr/bin/env python
#
# Stephen Patrick Vicchio
# 2019-06-30
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
# [JOB-CREATION.py] Creates the new submission files for a Gaussian restart
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
from datetime import datetime 
import subprocess 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   P A R A M E T E R S 

FAIL = '\033[91m'
ENDC = '\033[0m'

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# List of Directories

DIR_ = os.getcwd()
TEMPLATE_DIR = os.path.join('/common/curium/svicchi/00-MOF/zx-templates', 'JOB-CREATION-TEMPLATES')

SUBVASP_H = 'subvasp-multi-head.temp'
SUBVASP_T = 'subvasp-multi-tail.temp'
SUBVASP_M = 'subvasp-multi.temp' 

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

def checking_files_restart(dir_path, dir_check):
    
    dir_current = os.path.join(dir_path,dir_check)
    dir_list = os.listdir(dir_current)
    for dir_list_file in dir_list: 
        if dir_list_file.split('.')[-1] == 'log':
            log_status = True
        elif dir_list_file.split('.')[-1] == 'chk':
            chk_status = True
            
    return log_status, chk_status

def find_copy_file(dir_path,extension):
    dir_list = os.listdir(dir_path) 
    print(dir_list)
    for dir_list_file in dir_list: 
        if dir_list_file.split('.')[-1] == str(extension):
            file_copy = dir_list_file

    return file_copy
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
                        help='name of the directory to restart from')
    parser.add_argument('-c', action='store', dest='COUNT_CONT', default=int(4),
                        type=int, help='number of stages to create')
    parser.add_argument('-n', action='store', dest='NSW_COUNT', default=int(10),
                        type=int, help='number of NSW to take during each stage')
    parser.add_argument('-i', action='store', dest='ISTART', default=int(2), 
                        type=int, help='0: new WAVECAR, 2: old WAVECAR')
    parser.add_argument('-j', action='store', dest='JOBID', default=str(str(datetime.now()).split('.')[0]).replace(' ','-'))
    args = parser.parse_args()
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #       
# Determining the status of the current run 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  

    # Checking to make sure 
    try: 
        if os.path.isdir(os.path.join(DIR_, args.START_DIR)) is True: 
            restart_dir = os.path.join(DIR_, args.START_DIR)
            list_directories = os.listdir(restart_dir)
            for restart_dir_dirs in list_directories:
                if restart_dir_dirs == '00-opt':
                    opt_log, opt_chk = checking_files_restart(restart_dir,restart_dir_dirs)
                elif restart_dir_dirs == '01-stable':
                    stb_log, stb_chk = checking_files_restart(restart_dir,restart_dir_dirs)
                elif restart_dir_dirs == '02-freq':
                    frq_log, frq_chk = checking_files_restart(restart_dir,restart_dir_dirs)
                    frq_dir = os.path.join(restart_dir,'02-freq')
                    
    except IOError:
        sys.stderr.write(FAIL)
        sys.stderr.write("\nSomething is wrong with the files\n")
        sys.stderr.write(ENDC+"\n")
        sys.exit()
    
    try:
        new_number = str(int(args.START_DIR.split('-')[0]) + 1).zfill(2)
        JOB_COUNT_DICT[new_number]
        next_dir = str(new_number + '-' + JOB_COUNT_DICT[new_number] + '-stage')
        new_dir = os.path.join(DIR_,next_dir) 
        if new_dir not in os.listdir(DIR_):
            os.mkdir(new_dir)
            os.mkdir(os.path.join(new_dir,'za-previous'))
            if frq_log is True and frq_chk is True:
                os.mkdir(os.path.join(new_dir,'00-opt'))
        else:
            raise OSError
    except OSError:
        sys.stderr.write(FAIL)
        sys.stderr.write("\nERROR:The directory already exists...\n")      
        sys.stderr.write(ENDC+"\n")
        sys.exit()
    
        
    if frq_chk is True: 
        print('FREQ here we go...')
        copy_chk_file = find_copy_file(frq_dir,'chk')
        copy_com_file = find_copy_file(frq_dir,'com')
        print(copy_chk_file)
        print(copy_com_file)
        
    elif stb_chk is True:
        print('nah.. we doing stable...')
             
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T 
    
if __name__ == '__main__':
        main()
