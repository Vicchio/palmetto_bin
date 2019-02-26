#!/usr/bin/env python
#
# Stephen Patrick Vicchio
# 2019-02-23
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
import re 
import argparse
from optparse import OptionParser

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   P A R A M E T E R S 

FAIL = '\033[91m'
ENDC = '\033[0m'

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   F U N C T I O N 



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# M A I N   P R O G R A M  

def main():

    
    # Parsing the command line arguments
    parser = argparse.ArgumentParser(description="""\nThis script is designed 
                                     to parse VASP outcar files to provide 
                                     information on how each run converged.""")
    parser.add_argument('-i', action='store', dest='OUTCAR_file', 
                        help='OUTCAR file to be parsed')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')    
    args = parser.parse_args()
    
    
    try: 
        outcar = open(args.OUTCAR_file,"r")
    except IOError:
        sys.stderr.write(FAIL)
        sys.stderr.write("There was a problem opening the OUTCAR file. Does" /
                         "it exist at all?")
        sys.stderr.write(ENDC+"\n")
        sys.exit(1)
        
    if outcar != None:
        print('\nThere exists an OUTCAR file!\n')
        
        outcarfile = args.OUTCAR_file
        outcarlines = outcar.readlines()
        
        # Finding the max iterations
        NELMAX = int(subprocess.check_output(['grep', 'NELM', outcarfile]).split()[2][0:-1])
        NATOMS = int(subprocess.check_output(['grep', "NIONS", outcarfile]).split()[11])
        EDIFF = math.log10(float(subprocess.check_output(['grep','EDIFF  =', outcarfile]).split()[2]))
        
        # Generating the search parameters 
        
        re_iteration = re.compile('Iteration')
        re_force = re.compile('TOTAL-FORCE')
        re_timing = re.compile('LOOP:')
        re_volume = re.compile('volume of cell')
        re_mag = re.compile('number of electron')
        
        
        cputime_min = 0.0
        cputime_hrs = 0.0
        volume_val = None
        
        line_count = 0 
        electronic_count = 0 
        for line in outcarlines: 
            
            # Electronic optimization AND scf_count 
            if re_iteration.search(line):                
                scf_count = int(line.split()[3][0:-1])
                electronic_count = int(line.split()[2][0:-1])
            
                print(scf_count, electronic_count)
                
            # Computing Force Parameters
            if re_force.search(line):
                forces = []
                magnitudes = []
                for i in range(0,NATOMS):
                    raw_forces = outcarlines[line_count+i+2].split()
                    x_raw_force = float(raw_forces[3])
                    y_raw_force = float(raw_forces[4])
                    z_raw_force = float(raw_forces[5])
                    forces.append([x_raw_force, y_raw_force, z_raw_force])
                    magnitudes.append(math.sqrt(x_raw_force*x_raw_force + y_raw_force*y_raw_force + z_raw_force*z_raw_force))
                average_force = float(sum(magnitudes)/NATOMS)
                max_force = float(max(magnitudes))

# TODO: add to the script that shows the atom containing the maximum force  

            # Computes VASP runtimes for each step
            if re_timing.search(line):
                cputime_min += float(line.split()[6])/60.0
                cputime_hrs += float(line.split()[6])/3600
                
            # Computes the cell volume for each step
            if re_volume.search(line):
                if volume_val is None: 
                    volume_val = line.split()[4]
                elif volume_val != line.split()[4]:
                    volume_val = line.split()[4]
                    
            # Computes the magmom for the system 
            if re_mag.search(line):
                parts = line.split()
                if len(parts) > 5 and parts[0].strip() != "NELECT":
                    spinpolarized = True
                    magmom = float(parts[5])
                              
# TODO: Now I need to write the energies for each step and then format the
#       information properly... 
                
            
            
            
            
# TODO: Write a loop for all the data contained in the first electronic step 
            if electronic_count == 1: 
                if scf_count == 1 and electronic_count == 1: 
                    scf_data = []
                    raw_electronic = []
                    dif_electronic = []
                    
                    scf_data.append(int(scf_count))
                    raw_electronic.append(float(10))
                    dif_electronic.append(float(0))
                elif scf_count != 1 and electronic_count == 1:
                    scf_data.append(int(scf_count))
                    raw_electronic.append(float(4))
                    difference = abs(float(raw_electronic[-1] - raw_electronic[-2]))
                    dif_electronic.append(difference)
            elif electronic_count == 2:
# TODO: write all the dat a I want to store here for the first SCF step 
                print('The electronic count doesnt equal 1')
                print(scf_count)
                print(raw_electronic)
           
                
            line_count += 1
            
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T 
    
if __name__ == '__main__':
        main()