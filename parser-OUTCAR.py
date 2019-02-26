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

#def get_number_of_atoms(where):
#    return int(commands.getoutput("grep \"NIONS\" " + where).split()[11])
#
#def get_ediff(where):
#    return float(commands.getoutput("grep \"  EDIFF\" " + where).split()[2])


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
        
        line_count = 0 
        for line in outcarlines: 
            
            if re_iteration.search(line):                
                scf_count = int(line.split()[3][0:-1])
                electronic_count = int(line.split()[2][0:-1])
                
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
                    
                print('---------------------------------------------------')
                print(forces)
                print(magnitudes)
        
                    
            line_count += 1
                    
                    
            

#        outcarfile = args.OUTCAR_file
#        outcarlines = outcar.readlines()
#
#        # Find max iterations
#        nelmax = int(commands.getoutput("grep NELM " + outcarfile).split()[2][0:-1])
#        natoms = get_number_of_atoms(outcarfile)
#        ediff = math.log10(float(get_ediff(outcarfile)))



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T 
    
if __name__ == '__main__':
        main()