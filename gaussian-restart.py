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
    
    log_status = False
    chk_status = False
    
    dir_current = os.path.join(dir_path,dir_check)
    dir_list = os.listdir(dir_current)
    for dir_list_file in dir_list: 
        if dir_list_file.split('.')[-1] == 'log':
            log_status = True
        if dir_list_file.split('.')[-1] == 'chk':
            chk_status = True
            
    return log_status, chk_status

def find_copy_file(dir_path,extension):
    dir_list = os.listdir(dir_path) 
    for dir_list_file in dir_list: 
        if dir_list_file.split('.')[-1] == str(extension):
            file_copy = os.path.join(dir_path,dir_list_file)

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
            
            if '00-opt' in list_directories:
                opt_log, opt_chk = checking_files_restart(restart_dir,'00-opt')
                opt_dir = os.path.join(restart_dir,'00-opt')  
            if '02-freq' in list_directories:
                frq_log, frq_chk = checking_files_restart(restart_dir,'02-freq')
                frq_dir = os.path.join(restart_dir,'02-freq')
            else:
                frq_log = False
                frq_chk = False
            
            
#            for restart_dir_dirs in list_directories:               
#                if restart_dir_dirs == '00-opt':
#                    opt_log, opt_chk = checking_files_restart(restart_dir,restart_dir_dirs)
#                    opt_dir = os.path.join(restart_dir,'00-opt')  
#                elif restart_dir_dirs == '02-freq':
#                    frq_log, frq_chk = checking_files_restart(restart_dir,restart_dir_dirs)
#                    frq_dir = os.path.join(restart_dir,'02-freq')

    except IOError:
        sys.stderr.write(FAIL)
        sys.stderr.write("\nSomething is wrong with the files\n")
        sys.stderr.write(ENDC+"\n")
        sys.exit()
    
    print('opt',opt_log, opt_chk)
    print('freq',frq_log, frq_chk)
    try:
        new_number = str(int(args.START_DIR.split('-')[0]) + 1).zfill(2)
        JOB_COUNT_DICT[new_number]
        next_dir = str(new_number + '-' + JOB_COUNT_DICT[new_number] + '-stage')
        new_dir = os.path.join(DIR_,next_dir) 
        if new_dir not in os.listdir(DIR_):
            os.mkdir(new_dir)
            new_dir_prev = os.path.join(new_dir,'za-previous')
            os.mkdir(new_dir_prev)
            if frq_log is True and frq_chk is True:
                new_dir_opt = os.path.join(new_dir,'00-opt')
                os.mkdir(new_dir_opt)
        else:
            raise OSError
    except OSError:
        sys.stderr.write(FAIL)
        sys.stderr.write("\nERROR:The directory already exists...\n")      
        sys.stderr.write(ENDC+"\n")
        sys.exit()
    
    # copying com and chk files over to correct location    
    if frq_chk is True: 
        copy_chk_file = find_copy_file(frq_dir,'chk')
        copy_com_file = find_copy_file(frq_dir,'com')
        status_chk = True
    elif opt_chk is True: 
        copy_chk_file = find_copy_file(opt_dir,'chk')
        copy_com_file = find_copy_file(opt_dir,'com')
        status_chk = True

    # preparing chk file for the restart
    if status_chk is True: 
        copy2(copy_chk_file,new_dir_prev)
        copy2(copy_com_file,new_dir_prev)
    
        # copying the submission script and the basisset.tmp files
        copy_sub_file = find_copy_file(args.START_DIR,'sh')
        copy2(copy_sub_file,new_dir)
        copy2(os.path.join(args.START_DIR,'basisset.tmp'),new_dir)
        
        copy2(copy_chk_file,new_dir_opt)
        list_old_chk = os.listdir(new_dir_opt)[0].split('-')
        list_new_chk = list_old_chk[: len(list_old_chk) - 1] 
        list_new_chk.append('opt.chk')
        file_new_chk = os.path.join(new_dir_opt,'-'.join(list_new_chk))
        os.rename(os.path.join(new_dir_opt,'-'.join(list_old_chk)),file_new_chk)
    
        # preparing the gjf file for the restart 
        copy2(copy_com_file,os.path.join(new_dir,os.path.basename(copy_com_file)))
        list_old_com = os.path.basename(copy_com_file).split('-')
        list_new_com = list_old_com[: len(list_old_com) - 1] 
        file_new_gjf = os.path.join(new_dir,'-'.join(list_new_com) + '.gjf')
        os.rename(os.path.join(new_dir,os.path.basename(copy_com_file)),file_new_gjf)
        
        # modifying the gjf file to be the correct format 
        sed_cmd_geo = '/Geom=Connect/d'
        subprocess.call(['sed', '-i', sed_cmd_geo, file_new_gjf])
        
        with open(file_new_gjf, 'r') as new_gjf, open(os.path.join(new_dir,'basisset.tmp'),'r') as basis: 
            basis_lines = basis.readlines()
            file_new_gjf_lines = new_gjf.readlines()
        new_gjf.close()
        basis.close()
        file_new_gjf_combined = file_new_gjf_lines + basis_lines
        
        with open(os.path.join(new_dir,'temp-gjf-file'),'w') as write_file:
            for line in file_new_gjf_combined:
                write_file.write(line)
        write_file.close()
        
        os.rename(os.path.join(new_dir,'temp-gjf-file'),file_new_gjf)
    else:
        sys.stderr.write(FAIL)
        sys.stderr.write("\nError: can't perform restart run.\n")      
        sys.stderr.write(ENDC+"\n")
        sys.exit()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T 
    
if __name__ == '__main__':
        main()
