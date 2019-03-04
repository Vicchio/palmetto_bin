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
ATOMS_FORCE = 'Atom Forces'
MAGNITUDES = 'Magnitudes'
AVERAGE_FORCE ='Avg Force'
MAX_FORCE = 'Max Force'


DIR_ = os.getcwd()


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
    parser.add_argument('-w', action='store', dest='OUTPUT_SCF', default=False,
                        help='set as True to generate SCF convergence files')
    parser.add_argument('--version', action='version', version='%(prog)s 1.1.0')    
    args = parser.parse_args()
    
    if args.OUTPUT_SCF == 'True':
        args.OUTPUT_SCF = True 
    
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
        re_energy_dis = re.compile('Edisp')
        re_energy_scf = re.compile('  free energy =')
        re_end = re.compile('General timing and accounting informations for this job:')
        
        cputime_min = 0.0
        cputime_hrs = 0.0
        volume_val = None
        
        # List of starting variables
        magmom = None
        line_count = 0 
        electronic_count = 0 
        previous_electronic_step = 1 
        scf_count = 0 
        electronic_dict = {}
        force_dict = {}
        spinpolarized = False
        FINISH_RUN_STATUS = False
        
        for line in outcarlines: 
            # Electronic optimization AND scf_count 
            if re_iteration.search(line):                
                electronic_count = int(line.split()[2][0:-1])
                if electronic_count != previous_electronic_step:
                    # Time to write all the OUTPUTS!
                    stepstr = str(previous_electronic_step).rjust(4)
                    energystr = "Energy: " + ("%3.6f" % (electronic_dict[previous_electronic_step][ENERGY_KEY][-1])).rjust(12)
                    logdestr  = "Log|dE|: " + ("%1.3f" % (electronic_dict[previous_electronic_step][DIFF_KEY][-1])).rjust(6)					
                    iterstr   = "SCF: " + ("%3i" % (scf_count))
                    avgfstr   = "Avg|F|: " + ("%2.3f" % (force_dict[previous_electronic_step][AVERAGE_FORCE])).rjust(6)
                    volstr    = "Vol.: " + ("%3.1f" % (volume_val)).rjust(5)
                    maxfstr   = "Max|F|: " + ("%2.3f" % (force_dict[previous_electronic_step][MAX_FORCE])).rjust(6)
                    timehrstr   = "Time: " + ("%3.2fhr" % (cputime_min)).rjust(6)
                    if spinpolarized is True:
                        magstr="Mag: " + ("%2.2f" % (magmom)).rjust(6)
                        print(stepstr, energystr, logdestr, iterstr, avgfstr, maxfstr, volstr, magstr, timehrstr)
                    else:
                        print(stepstr, energystr, logdestr, iterstr, avgfstr, maxfstr, timehrstr)                
                    
                scf_count = int(line.split()[3][0:-1])
                cputime_min = 0.0
                cputime_hrs = 0.0 
                previous_electronic_step = electronic_count 
                
    # THIS PORTION OF THE CODE DOES ALL THE PARSING
    
                # Creates the flags to search OUTCAR File
                if electronic_count == 1: 
                    re_energy_scf = re.compile('free energy    TOTEN')
                    ENERGY_GRAB = 4
                else: 
                    re_energy_scf = re.compile('  free energy =')
                    ENERGY_GRAB = 3
                    
            # Computing Force Parameters
            if re_force.search(line):
                if electronic_count not in force_dict.keys():
                    # Generates the force dict 
                    force_dict[electronic_count] = {}
                    force_dict[electronic_count][ATOMS_FORCE] = []
                    force_dict[electronic_count][MAGNITUDES] = []
                for i in range(0,NATOMS):
                    raw_forces = outcarlines[line_count+i+2].split()
                    x_raw_force = float(raw_forces[3])
                    y_raw_force = float(raw_forces[4])
                    z_raw_force = float(raw_forces[5])
                    force_dict[electronic_count][ATOMS_FORCE].append([x_raw_force, y_raw_force, z_raw_force])
                    force_dict[electronic_count][MAGNITUDES].append(math.sqrt(x_raw_force*x_raw_force + y_raw_force*y_raw_force + z_raw_force*z_raw_force))
                
                force_dict[electronic_count][AVERAGE_FORCE] = float(sum(force_dict[electronic_count][MAGNITUDES])/NATOMS)
                force_dict[electronic_count][MAX_FORCE] = float(max(force_dict[electronic_count][MAGNITUDES]))

# TODO: add to the script that shows the atom containing the maximum force  

            # Computes VASP runtimes for each step
            if re_timing.search(line):
                cputime_min += float(line.split()[6])/60.0
                cputime_hrs += float(line.split()[6])/3600
                
            # Computes the cell volume for each step
            if re_volume.search(line):
                if volume_val is None: 
                    volume_val = float(line.split()[4])
                elif volume_val != line.split()[4]:
                    volume_val = float(line.split()[4])
                    
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
            
#            if re_energy_dis.search(line):
#                print(line.split()[2])
                
            # Checks to see if the end of the file is there
            if re_end.search(line):
                FINISH_RUN_STATUS = True
            
            line_count += 1 #IMPORTANT: required for finding 
            
        # if the end of the file exists, this prints the last SC step 
        if FINISH_RUN_STATUS is True:            
            stepstr = str(previous_electronic_step).rjust(4)
            energystr = "Energy: " + ("%3.6f" % (electronic_dict[previous_electronic_step][ENERGY_KEY][-1])).rjust(12)
            logdestr  = "Log|dE|: " + ("%1.3f" % (electronic_dict[previous_electronic_step][DIFF_KEY][-1])).rjust(6)					
            iterstr   = "SCF: " + ("%3i" % (scf_count))
            avgfstr   = "Avg|F|: " + ("%2.3f" % (force_dict[previous_electronic_step][AVERAGE_FORCE])).rjust(6)
            volstr    = "Vol.: " + ("%3.1f" % (volume_val)).rjust(5)
            maxfstr   = "Max|F|: " + ("%2.3f" % (force_dict[previous_electronic_step][MAX_FORCE])).rjust(6)
            timehrstr   = "Time: " + ("%3.2fhr" % (cputime_hrs)).rjust(6)
            if spinpolarized is True:
                magstr="Mag: " + ("%2.2f" % (magmom)).rjust(6)
                print(stepstr, energystr, logdestr, iterstr, avgfstr, maxfstr, volstr, magstr, timehrstr)
            else:
                print(stepstr, energystr, logdestr, iterstr, avgfstr, maxfstr, timehrstr)          

            
    if args.OUTPUT_SCF is True: 
        working_dir = os.path.join(DIR_, 'zz-OUTCAR-parse')
        if not os.path.exists(os.path.join(DIR_, 'zz-OUTCAR-parse')):
            os.makedirs(os.path.join(DIR_, 'zz-OUTCAR-parse'))

        for electronic_ in electronic_dict.keys():
            xlength = 300 
            if electronic_ == 1:
                filename = 'conv-elec-step-' + str(electronic_).zfill(3) 
                plt.figure()
                plt.title('Convergence for ' + str(electronic_).zfill(3) + ' Electronic step')
                plt.scatter(electronic_dict[electronic_][SCF_KEY], electronic_dict[electronic_][DIFF_KEY])
                plt.plot(list(range(0,xlength)), np.full((xlength,1),EDIFF), color='red', linestyle='dashed')
                plt.annotate(xy=[xlength,EDIFF],s='EDIFF = 10^'+ str(EDIFF), xytext=(xlength-85,EDIFF*0.9))
                plt.annotate(s='Convergence in\n' + str(electronic_dict[electronic_][SCF_KEY][-1]) + ' steps',
                             xy=[electronic_dict[electronic_][SCF_KEY][-1],electronic_dict[electronic_][DIFF_KEY][-1]],
                             xytext=[electronic_dict[electronic_][SCF_KEY][-1] + 10,electronic_dict[electronic_][DIFF_KEY][-1]])
#                plt.plot(electronic_dict[electronic_][SCF_KEY], np.full((len(electronic_dict[electronic_][SCF_KEY]),1),EDIFF), color='red', linestyle='dashed')
                plt.axis([0, 300, math.log10(1e-8), math.log10(1e6)])
                plt.xlabel('SCF Iteration #')
                plt.ylabel('Log|dE|')         
                plt.yticks(np.arange(math.log10(1e-8), math.log10(1e7), step = 2))
                plt.savefig(os.path.join(working_dir, filename) + '.png')
                


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T 
    
if __name__ == '__main__':
        main()