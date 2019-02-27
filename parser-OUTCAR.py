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

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   P A R A M E T E R S 

FAIL = '\033[91m'
ENDC = '\033[0m'

ENERGY_KEY = 'Electronic Energy'
SCF_KEY = 'SCF Count' 
DIFF_KEY = 'Difference Energy'

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
    parser.add_argument('-w', action='store', dest='OUTPUT-TYPE', default=False,
                        help='set as True to generate SCF convergence files')
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
        re_energy_dis = re.compile('Edisp (eV)')
        re_energy_scf = re.compile('  free energy =')
        
        cputime_min = 0.0
        cputime_hrs = 0.0
        volume_val = None
        
        # List of starting variables  
        line_count = 0 
        electronic_count = 0 
        current_electronic_count = 1 
        scf_count = 0 
        electronic_dict = {}
        electronic_status = True
        
        for line in outcarlines: 
            # Electronic optimization AND scf_count 
            if re_iteration.search(line):                
                scf_count = int(line.split()[3][0:-1])
                electronic_count = int(line.split()[2][0:-1])
                if electronic_count != current_electronic_count:
                    electronic_status = False
                current_electronic_count = electronic_count 
                
                # Creates the flags to search OUTCAR File
                if electronic_count == 1: 
                    re_energy_scf = re.compile('free energy    TOTEN')
                    ENERGY_GRAB = 4
                else: 
                    re_energy_scf = re.compile('  free energy =')
                    ENERGY_GRAB = 3
                    
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
                    
            # Computes the electronic energy search of POSCAR file
            if re_energy_scf.search(line):
                if electronic_count not in electronic_dict.keys():
                    # Generates the dictionary information for the run
                    electronic_dict[electronic_count] = {}
                    electronic_dict[electronic_count][SCF_KEY] = []
                    electronic_dict[electronic_count][ENERGY_KEY] = []
                    electronic_dict[electronic_count][DIFF_KEY] = []
                 
                # writes the electronic parameters
                electronic_dict[electronic_count][SCF_KEY].append(int(scf_count))                
                electronic_dict[electronic_count][ENERGY_KEY].append(float(line.split()[ENERGY_GRAB]))
                
                # generates and write the differences in electronic steps
                if scf_count == 1:
                    difference = float(0.0)
                else:
                    difference = math.log10(abs(electronic_dict[electronic_count][ENERGY_KEY][-1] - electronic_dict[electronic_count][ENERGY_KEY][-2]))
                electronic_dict[electronic_count][DIFF_KEY].append(difference)
            
            
            # writing the OUTPUTS
            if electronic_status is False: 
                print(electronic_count, scf_count)
                stepstr = str(electronic_count).rjust(4)
#    				energystr = "Energy: " + ("%3.6f" % (energy)).rjust(12)
#    				logdestr = "Log|dE|: " + ("%1.3f" % (dE)).rjust(6)					
                iterstr = "SCF: " + ("%3i" % (scf_count))
                avgfstr="Avg|F|: " + ("%2.3f" % (average_force)).rjust(6)
                maxfstr="Max|F|: " + ("%2.3f" % (max_force)).rjust(6)
                timestr="Time: " + ("%3.2fm" % (cputime_min)).rjust(6)
#                 
#                    
                print(stepstr, iterstr, avgfstr, maxfstr, timestr)
#                
                
#                except NameError:
#                    print("Cannot understand this OUTCAR file...try to read ahead")
#                    continue 
#                
            # resets te electronic status as True to avoid OUTPUT loop
                electronic_status = True 
        
            
            
            
            
# TODO: Now I need to write the energies for each step and then format the
#       information properly... 
#                
#            
#            if electronic_count == 1: 
#                if scf_count == 1 and electronic_count == 1: 
#                    scf_data = []
#                    raw_electronic = []
#                    dif_electronic = []
#                    
#                    scf_data.append(int(scf_count))
#                    raw_electronic.append(float(10))
#                    dif_electronic.append(float(0))
#                elif scf_count != 1 and electronic_count == 1:
#                    scf_data.append(int(scf_count))
#                    raw_electronic.append(float(4))
#                    difference = abs(float(raw_electronic[-1] - raw_electronic[-2]))
#                    dif_electronic.append(difference)
#            elif scf_count == 1 and electronic_count == 2:
## TODO: write all the dat a I want to store here for the first SCF step 
#                pass
            
                
            line_count += 1
            
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T 
    
if __name__ == '__main__':
        main()