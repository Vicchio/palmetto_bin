#!/usr/bin/env python
#
# Stephen Patrick Vicchio
# 2019-07-06
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
# [parser-OUTCAR.py] parses the OUTCAR file generated from VASP to produce 
# information on the SCF convergence of each step, average force, maximum 
# force, etc. The script is designed to help understand convergence runs in 
# VASP. 
#
# Note: This script is a modified version of a script (grad2.py) written by 
# Peter Larsson. The original can be found at: 
# https://www.nsc.liu.se/~pla/vasptools/. 
#
# Peter Larsson constructed the orginal script (AS MENTIONED ABOVE). I needed 
# the script to perform similar operations, and I noticed a small error in his
# orginal script that I wanted to correct. I DO NOT take credit for the
# algorithms generated here.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
#  INPUT: OUTCAR file from VASP 
# OUTPUT: information on the SCF convergence, max force, etc. 
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# L I S T   O F   I M P O R T S 
import subprocess 
import os 
import sys
import math
import numpy as np 
import re 
import argparse
import matplotlib.pyplot as plt

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   P A R A M E T E R S 

FAIL = '\033[91m'
ENDC = '\033[0m'

ENERGY_KEY = 'Electronic Energy'
SCF_KEY = 'SCF Count' 
DIFF_KEY = 'Difference Energy'
ATOMS_FORCE_RAW = 'Atom Forces'
MAGNITUDES = 'Magnitudes'
AVERAGE_FORCE ='Avg Force'
MAX_FORCE = 'Max Force'
MAX_ATOM = 'Max Atom'
PARSER_FILE = 'aa-parser-info.txt' 
ATOM_COUNT = 'Atom Count'
TOTEN_ENERGY = 'Free Energy Toten'
DIS_ENERGY   = 'Dispersion Energy'
SIGMA_ENERGY = 'energy(sigma->0)'
NO_ENTROPY_ENERGY = 'ENERGY WITHOUT ENTROPY'
VASP_MAX_FORCE = 'VASP MAX FORCE'
VASP_RMS_FORCE = 'VASP RMS FORCE'
CONVERT_RAW_FORCE = 'CONVERT_FORCE_RAW'
X_COORDS    = 'X_COORDS'
Y_COORDS    = 'Y_COORDS'
Z_COORDS    = 'Z_COORDS'
X_FORCES    = 'X_FORCES'
Y_FORCES    = 'Y_FORCES'
Z_FORCES    = 'Z_FORCES'
NUMBER      = 'ATOM NUMBER'
RELAX       = 'ATOM RELAX?'
RMS_FORCE   = 'RMS FORCES'
FREE_ENERGY_TOTEN = 'free  energy   TOTEN'


DIR_ = os.getcwd()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   F U N C T I O N S



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# M A I N   P R O G R A M  

def main():
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #       
# command line arguments 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #   

    # Parsing the command line arguments
    parser = argparse.ArgumentParser(description="""\n
                        This script is designed to parser a CP2K output file 
                        to check for convergence. The script will determine how
                        the calculation performed.\n""")
    parser.add_argument('-i', action='store', dest='CP2K_OUTPUT_FILE', 
                        default=None, help='CP2K output file to parse')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    args = parser.parse_args()

    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #       
# checking the OUT file for CP2K
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #   


    #CP2K_OUTPUT_FILE = os.path.join("C:\\Users\\svicchi\Desktop",'1ni3-nu-1000-bare.out')
    CP2K_OUTPUT_FILE = os.path.join(DIR_,args.CP2K_OUTPUT_FILE)
    
    if os.path.isfile(CP2K_OUTPUT_FILE) is True:
        try:
            CP2K_out = open(CP2K_OUTPUT_FILE)
        except IOError:
            sys.stderr.write(FAIL)
            sys.stderr.write("Is the .out file around?")
            sys.stderr.write(ENDC+"\n")
            sys.exit(1)
                
 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #       
# First read of the CP2K output file 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 
    FINISHED_STATUS = False
    
    with open(CP2K_OUTPUT_FILE, 'r') as CP2K_file:        
        # defining the search parameters for the CP2K file
        re_opt_step_    = re.compile('OPTIMIZATION STEP: ')
        re_step_infor   = re.compile('--------  Informations at step =')

        K_TOTAL_ENERGY  = 'Total Energy               ='
        re_TOTAL_ENERGY = re.compile(K_TOTAL_ENERGY)

        K_REAL_E_CHANG  = 'Real energy change         ='
        re_REAL_E_CHANG = re.compile(K_REAL_E_CHANG)
    
        K_DECRE_ENERGY  = 'Decrease in energy         ='
        re_DECRE_ENERGY = re.compile(K_DECRE_ENERGY)

        K_USED_TIME_JO  = 'Used time                  ='
        re_USED_TIME_JO = re.compile(K_USED_TIME_JO)

        K_MAX_STEP_SIZ  = 'Max. step size             ='
        re_MAX_STEP_SIZ = re.compile(K_MAX_STEP_SIZ)

        K_CONV_MAX_STEP  = 'Convergence in step size   ='
        re_CONV_MAX_STEP = re.compile(K_CONV_MAX_STEP)

        K_CONV_RMS_STEP  = 'Convergence in RMS step    ='
        re_CONV_RMS_STEP = re.compile(K_CONV_RMS_STEP)

        K_CONV_GRAD      = 'Conv. for gradients        ='
        re_CONV_GRAD     = re.compile(K_CONV_GRAD)
        K_CONV_MAX_GRAD  = 'CONVERGENCE_MAX_GRAD'
        K_CONV_RMS_GRAD  = 'CONVERGENCE_RMS_GRAD'
        
        re_CONV_GRAD_RMS = re.compile(' Conv. in RMS gradients     =')
        re_CONV_GRAD_MAX = re.compile(' Conv. for gradients        =')
        
        K_RMS_STEP_SIZ  = 'RMS step size              ='
        re_RMS_STEP_SIZ = re.compile(K_RMS_STEP_SIZ)

        K_MAX_GRADIENT  = 'Max. gradient              ='
        re_MAX_GRADIENT = re.compile(K_MAX_GRADIENT)

        K_RMS_GRADIENT  = 'RMS gradient               ='
        re_RMS_GRADIENT = re.compile(K_RMS_GRADIENT)       
    

    
        K_FINISHED_JOB  = "  \*\*\*\* \*\*\*\* \*\*\*\*\*\*  \*\*  PROGRAM ENDED AT"
        re_FINISHED_JOB = re.compile(K_FINISHED_JOB)
        
    
        # General parameters for the parser
        INFORMATION_DICT = {}
        NUM_DIGITS = 6         

        # checking the line information for the job
        for line_no, line in enumerate(CP2K_file):
            
            # setting up the informationd dict for the specific step           
            if re_step_infor.search(line):
                CURRENT_KEY = line
                INFORMATION_DICT[CURRENT_KEY] = {}
                INFORMATION_DICT[CURRENT_KEY]['OPT-key']      = int(CURRENT_KEY.split()[5])
                INFORMATION_DICT[CURRENT_KEY][K_TOTAL_ENERGY] = None
                INFORMATION_DICT[CURRENT_KEY][K_REAL_E_CHANG] = None
                INFORMATION_DICT[CURRENT_KEY][K_DECRE_ENERGY] = 'N/a'
                INFORMATION_DICT[CURRENT_KEY][K_USED_TIME_JO] = None
                INFORMATION_DICT[CURRENT_KEY][K_MAX_STEP_SIZ] = None
                INFORMATION_DICT[CURRENT_KEY][K_RMS_STEP_SIZ] = None
                INFORMATION_DICT[CURRENT_KEY][K_MAX_GRADIENT] = None
                INFORMATION_DICT[CURRENT_KEY][K_RMS_GRADIENT] = None
                INFORMATION_DICT[CURRENT_KEY][K_CONV_MAX_STEP] = 'N/a'
                INFORMATION_DICT[CURRENT_KEY][K_CONV_RMS_STEP] = 'N/a'
                INFORMATION_DICT[CURRENT_KEY][K_CONV_MAX_GRAD] = 'N/a'
                INFORMATION_DICT[CURRENT_KEY][K_CONV_RMS_GRAD] = 'N/a'
                FIRST  = True
                SECOND = False
            
            if re_TOTAL_ENERGY.search(line):
                INFORMATION_DICT[CURRENT_KEY][K_TOTAL_ENERGY] = line.split()[3]
                
            if re_REAL_E_CHANG.search(line):
                INFORMATION_DICT[CURRENT_KEY][K_REAL_E_CHANG] = round(float(line.split()[4]),NUM_DIGITS)
                
            if re_DECRE_ENERGY.search(line):
                INFORMATION_DICT[CURRENT_KEY][K_DECRE_ENERGY] = line.split()[4]
                
            if re_USED_TIME_JO.search(line):
                INFORMATION_DICT[CURRENT_KEY][K_USED_TIME_JO] = round(float(line.split()[3]),NUM_DIGITS) 
                
            if re_MAX_STEP_SIZ.search(line):
                INFORMATION_DICT[CURRENT_KEY][K_MAX_STEP_SIZ] = round(float(line.split()[4]),NUM_DIGITS) 
                
            if re_CONV_MAX_STEP.search(line): 
                INFORMATION_DICT[CURRENT_KEY][K_CONV_MAX_STEP] = str(line.split()[5])
                
            if re_RMS_STEP_SIZ.search(line):
                INFORMATION_DICT[CURRENT_KEY][K_RMS_STEP_SIZ] = round(float(line.split()[4]),NUM_DIGITS) 
                
            if re_CONV_RMS_STEP.search(line):
                INFORMATION_DICT[CURRENT_KEY][K_CONV_RMS_STEP] = str(line.split()[5])

            if re_MAX_GRADIENT.search(line):
                INFORMATION_DICT[CURRENT_KEY][K_MAX_GRADIENT] = round(float(line.split()[3]),NUM_DIGITS)
                
            if re_CONV_GRAD.search(line):
                if FIRST is True and SECOND is False: 
                    INFORMATION_DICT[CURRENT_KEY][K_CONV_MAX_GRAD] = str(line.split()[4])
                    FIRST  = False
                    SECOND = True
                elif FIRST is False and SECOND is True: 
                    INFORMATION_DICT[CURRENT_KEY][K_CONV_RMS_GRAD] = str(line.split()[4])
            
            if re_CONV_GRAD_RMS.search(line):
                INFORMATION_DICT[CURRENT_KEY][K_CONV_RMS_GRAD] = str(line.split()[5])
            
            if re_CONV_GRAD_MAX.search(line):
                INFORMATION_DICT[CURRENT_KEY][K_CONV_MAX_GRAD] = str(line.split()[4])
                print(line)

            if re_RMS_GRADIENT.search(line):
                INFORMATION_DICT[CURRENT_KEY][K_RMS_GRADIENT] = round(float(line.split()[3]),NUM_DIGITS) 

            if re_FINISHED_JOB.search(line):
                FINISHED_STATUS = True
            
    CP2K_file.close()
          
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #       
# Printing out the information for the CP2K file
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #                    
        
    print('\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n') 

    str_step     = str('Step').ljust(8)
    str_energy   = str('Total Energy').ljust(18)
    str_e_change = str('Energy Change').ljust(18)
    str_max_size = str('Max Step').ljust(18)
    str_rms_size = str('RMS Step').ljust(18)
    str_max_grad = str('Max Gradient').ljust(18)
    str_rms_grad = str('RMS Gradient').ljust(18)
    
    print(str_step, str_energy, str_e_change, str_max_size, str_rms_size, str_max_grad, str_rms_grad)
    
    str_step     = str('----').ljust(6)
    str_energy   = str('-----------------').center(18)
    str_e_change = str('-----------------').center(18)
    str_max_size = str('---------------').center(18)
    str_rms_size = str('---------------').center(18)
    str_max_grad = str('---------------').center(18)
    str_rms_grad = str('---------------').center(18)
    
    print(str_step, str_energy, str_e_change, str_max_size, str_rms_size, str_max_grad, str_rms_grad)

    
    for INFO_KEYS in INFORMATION_DICT.keys():
        str_step     = str(INFORMATION_DICT[INFO_KEYS]['OPT-key']).zfill(3).center(6)
        str_energy   = str(INFORMATION_DICT[INFO_KEYS][K_TOTAL_ENERGY]).rjust(16)
        str_e_change = (str(INFORMATION_DICT[INFO_KEYS][K_REAL_E_CHANG]).ljust(10,'0') + str(' (' + INFORMATION_DICT[INFO_KEYS][K_DECRE_ENERGY] + ')').rjust(6)).rjust(18)
        
        if INFORMATION_DICT[INFO_KEYS]['OPT-key'] != 0:
            if INFORMATION_DICT[INFO_KEYS][K_REAL_E_CHANG] < 0: 
                str_e_change = (str(INFORMATION_DICT[INFO_KEYS][K_REAL_E_CHANG]).ljust(10,'0') + str(' (' + INFORMATION_DICT[INFO_KEYS][K_DECRE_ENERGY] + ')').rjust(6)).rjust(18)
            elif INFORMATION_DICT[INFO_KEYS][K_REAL_E_CHANG] > 0: 
                str_e_change = (str(INFORMATION_DICT[INFO_KEYS][K_REAL_E_CHANG]).ljust(9,'0') + str(' (' + INFORMATION_DICT[INFO_KEYS][K_DECRE_ENERGY] + ')').rjust(6)).rjust(18)

#            str_max_size = ("%1.6f" % float((INFORMATION_DICT[INFO_KEYS][K_RMS_STEP_SIZ]))).rjust(18)
            str_max_size = (str(INFORMATION_DICT[INFO_KEYS][K_MAX_STEP_SIZ]).ljust(8,'0') + str(' (' + INFORMATION_DICT[INFO_KEYS][K_CONV_MAX_STEP] + ')').rjust(6)).rjust(18)
            str_rms_size = (str(INFORMATION_DICT[INFO_KEYS][K_RMS_STEP_SIZ]).ljust(8,'0') + str(' (' + INFORMATION_DICT[INFO_KEYS][K_CONV_RMS_STEP] + ')').rjust(6)).rjust(18)
            str_max_grad = (str(INFORMATION_DICT[INFO_KEYS][K_MAX_GRADIENT]).ljust(8,'0') + str(' (' + INFORMATION_DICT[INFO_KEYS][K_CONV_MAX_GRAD] + ')').rjust(6)).rjust(18)
            str_rms_grad = (str(INFORMATION_DICT[INFO_KEYS][K_RMS_GRADIENT]).ljust(8,'0') + str(' (' + INFORMATION_DICT[INFO_KEYS][K_CONV_RMS_GRAD] + ')').rjust(6)).rjust(18)
        else:
            str_e_change = str('None').center(18)
            str_max_size = str('None').center(18)
            str_rms_size = str('None').center(18)
            str_max_grad = str('None').center(18)
            str_rms_grad = str('None').center(18)
            
        
        print(str_step, str_energy, str_e_change, str_max_size, str_rms_size, str_max_grad, str_rms_grad)

    print('\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n') 
    
    if FINISHED_STATUS is True: 
        print('The job finished. Check for convergence.')
        print('\n')
        
##        
#    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T 
    
if __name__ == '__main__':
        main()
        
        
        
        
        
   