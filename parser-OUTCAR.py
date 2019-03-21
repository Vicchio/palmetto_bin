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
ATOMS_FORCE_RAW = 'Atom Forces'
MAGNITUDES = 'Magnitudes'
AVERAGE_FORCE ='Avg Force'
MAX_FORCE = 'Max Force'
MAX_ATOM = 'Max Atom'
PARSER_FILE = 'aa-parser-info.txt' 
ATOM_COUNT = 'Atom Count'

DIR_ = os.getcwd()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   F U N C T I O N S

def atom_index_creation(atom_string, atom_count): 
    
    
    dict_atom = {}
    list_atom_order = []

    for catom in range(0, len(atom_string.split())):
        dict_atom[atom_string.split()[catom]] = atom_count.split()[catom]
    
    start = 0 
    for atom_key in dict_atom.keys():
        for i in range(start, int(dict_atom[atom_key]) + start):
            list_atom_order.append(str(atom_key).rjust(2) + '(' + str(i).zfill(3) + ')')
        start = i + 1
    
    return list_atom_order 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# M A I N   P R O G R A M  

def main():
    # Parsing the command line arguments
    parser = argparse.ArgumentParser(description="""\nThis script is designed 
                                     to parse VASP outcar files to provide 
                                     information on how each run converged.""")
    parser.add_argument('-i', action='store', dest='OUTCAR_file', default=None,
                        help='OUTCAR file to be parsed')
    parser.add_argument('-w', action='store', dest='OUTPUT_SCF', default=False,
                        help='set as True to generate SCF convergence files')
    parser.add_argument('-d', action='store', dest='STOP_DISPLAY', default=False,
                        help='set to True to stop display in terminal' )
    parser.add_argument('-forces', action='store', dest='WRITE_FORCES', default=False,
                        help='determines whether or not to write the forces')
    parser.add_argument('--version', action='version', version='%(prog)s 1.1.1')    
    args = parser.parse_args()
    
    if args.OUTPUT_SCF == 'True':
        args.OUTPUT_SCF = True 
    if args.STOP_DISPLAY == 'True':
        args.STOP_DISPLAY = True 
    if args.WRITE_FORCES == 'True':
       args.WRITE_FORCES = True  

    if os.path.isfile(args.OUTCAR_file) is True: 
        READFILE = args.OUTCAR_file
#    elif os.path.isfile('OUTCAR') is True:
#        READFILE = 'OUTCAR'
        
        
    if os.path.isfile('POSCAR') is True:
        POSCARFILE = 'POSCAR'
        
    try: 
        outcar = open(READFILE,"r")
    except IOError:
        sys.stderr.write(FAIL)
        sys.stderr.write("There was a problem opening the OUTCAR file. Does" /
                         "it exist at all?")
        sys.stderr.write(ENDC+"\n")
        sys.exit(1)
    
    try: 
        poscar = open(POSCARFILE,"r")
    except IOError:
        sys.stderr.write(FAIL)
        sys.stderr.write("Where is your POSCAR file?")
        sys.stderr.write(ENDC+"\n")
        sys.exit(1)
        
    if poscar != None:
        with open(POSCARFILE, 'r') as poscar_file: 
            poscarlines = poscar_file.readlines()          
            for pcount in range(0, 20):
                if pcount == 1:
                    SCALING_FACTOR = float(poscarlines[pcount].split()[0])
                elif pcount == 2:
                    ax = float(poscarlines[pcount].split()[0]) 
                    ay = float(poscarlines[pcount].split()[1])
                    az = float(poscarlines[pcount].split()[2])
                elif pcount == 3:
                    bx = float(poscarlines[pcount].split()[0])
                    by = float(poscarlines[pcount].split()[1])
                    bz = float(poscarlines[pcount].split()[2])
                elif pcount == 4:
                    cx = float(poscarlines[pcount].split()[0])
                    cy = float(poscarlines[pcount].split()[1])
                    cz = float(poscarlines[pcount].split()[2])
                elif pcount == 5:
                    atom_index = str(poscarlines[pcount])
                elif pcount == 6: 
                    atom_count = str(poscarlines[pcount])
        poscar_file.close()

        convert_M = np.array([[ax, ay, az], 
                              [bx, by, bz],
                              [cx, cy, cz]])
    
        list_atoms = atom_index_creation(atom_index, atom_count)


#NEED TO ADD MAJOR THINGS HERE. 

    
    if outcar != None:             
        parser_file_write = open(os.path.join(DIR_, PARSER_FILE), 'w')
        parser_file_write.write('\n')
        
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
        time_dict = {}
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
                    atomstr   = "Atom: " + str(force_dict[previous_electronic_step][MAX_ATOM]).rjust(6)
                    timehrstr   = "Time: " + ("%3.2fhr" % (time_dict[previous_electronic_step]['hours'])).rjust(6)
                    
    
                    if args.STOP_DISPLAY is True:                
                        if spinpolarized is True:
                            magstr="Mag: " + ("%2.2f" % (magmom)).rjust(6)
                            parser_file_write.write(stepstr + ' ' + energystr + ' ' + logdestr + ' ' + iterstr + ' ' + avgfstr + ' ' + maxfstr + ' ' + atomstr + ' ' + volstr + ' ' + magstr + ' ' + timehrstr+ '\n')
                        else:
                            parser_file_write.write(str(stepstr + energystr + logdestr + iterstr + avgfstr + maxfstr + atomstr + volstr + timehrstr) + '\n')
                    else: 
                        if spinpolarized is True:
                            magstr="Mag: " + ("%2.2f" % (magmom)).rjust(6)
                            print(stepstr, energystr, logdestr, iterstr, avgfstr, maxfstr, atomstr, volstr, magstr, timehrstr)
                            parser_file_write.write(stepstr + ' ' + energystr + ' ' + logdestr + ' ' + iterstr + ' ' + avgfstr + ' ' + maxfstr + ' ' + atomstr + ' ' + volstr + ' ' + magstr + ' ' + timehrstr+ '\n')
                        else:
                            print(stepstr, energystr, logdestr, iterstr, avgfstr, maxfstr, atomstr, volstr, timehrstr)       
                            parser_file_write.write(str(stepstr + energystr + logdestr + iterstr + avgfstr + maxfstr + atomstr + volstr + timehrstr) + '\n') 
                    
                        
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
                    force_dict[electronic_count][ATOM_COUNT] = []
                    force_dict[electronic_count][ATOMS_FORCE_RAW] = []
                    force_dict[electronic_count][MAGNITUDES] = []
                    
                for i in range(0,NATOMS):
                    raw_forces = outcarlines[line_count+i+2].split()
                    x_raw_force = float(raw_forces[3])
                    y_raw_force = float(raw_forces[4])
                    z_raw_force = float(raw_forces[5])
                    force_dict[electronic_count][ATOM_COUNT].append(list_atoms[i])
                    force_dict[electronic_count][ATOMS_FORCE_RAW].append([x_raw_force, y_raw_force, z_raw_force])
                    fractional_array = np.array([[x_raw_force],
                                                 [y_raw_force],
                                                 [z_raw_force]])



                    force_dict[electronic_count][MAGNITUDES].append(math.sqrt(x_raw_force*x_raw_force + y_raw_force*y_raw_force + z_raw_force*z_raw_force))
                
                
                magnitude_force = convert_M * fractional_array
                print(magnitude_force)
                print(magnitude_force.shape)
                
                force_dict[electronic_count][AVERAGE_FORCE] = float(sum(force_dict[electronic_count][MAGNITUDES])/NATOMS)
                force_dict[electronic_count][MAX_FORCE] = float(max(force_dict[electronic_count][MAGNITUDES]))
                force_dict[electronic_count][MAX_ATOM] = force_dict[electronic_count][ATOM_COUNT][force_dict[electronic_count][MAGNITUDES].index(max(force_dict[electronic_count][MAGNITUDES]))]
                
            # Computes VASP runtimes for each step
            if re_timing.search(line):
                if electronic_count not in time_dict.keys():
                    time_dict[electronic_count] = {}
                    time_dict[electronic_count]['hours'] = 0.0
                    time_dict[electronic_count]['minutes'] = 0.0
                
                time_dict[electronic_count]['minutes'] += float(line.split()[6])/60.0
                time_dict[electronic_count]['hours'] += float(line.split()[6])/3600.0
               
                
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
                elif abs(electronic_dict[electronic_count][ENERGY_KEY][-1]) == abs(electronic_dict[electronic_count][ENERGY_KEY][-2]):
                    difference = math.log10(abs(electronic_dict[electronic_count][ENERGY_KEY][-1] - electronic_dict[electronic_count][ENERGY_KEY][-2]) + 0.000000001)
                else: 
                    difference = math.log10(abs(electronic_dict[electronic_count][ENERGY_KEY][-1] - electronic_dict[electronic_count][ENERGY_KEY][-2]))
                electronic_dict[electronic_count][DIFF_KEY].append(difference)
                                      
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
            atomstr   = "Atom: " + str(force_dict[previous_electronic_step][MAX_ATOM]).rjust(6)
            timehrstr   = "Time: " + ("%3.2fhr" % (time_dict[previous_electronic_step]['hours'])).rjust(6)
            if args.STOP_DISPLAY is True:                
                if spinpolarized is True:
                    magstr="Mag: " + ("%2.2f" % (magmom)).rjust(6)
                    parser_file_write.write(stepstr + ' ' + energystr + ' ' + logdestr + ' ' + iterstr + ' ' + avgfstr + ' ' + maxfstr + ' ' + atomstr + ' ' + volstr + ' ' + magstr + ' ' + timehrstr+ '\n')
                    parser_file_write.write('\n')
                else:
                    parser_file_write.write(str(stepstr + energystr + logdestr + iterstr + avgfstr + maxfstr + atomstr + volstr + timehrstr) + '\n')
                    parser_file_write.write('\n')
            else: 
                if spinpolarized is True:
                    magstr="Mag: " + ("%2.2f" % (magmom)).rjust(6)
                    print(stepstr, energystr, logdestr, iterstr, avgfstr, maxfstr, atomstr, volstr, magstr, timehrstr)
                    print('')
                    parser_file_write.write(stepstr + ' ' + energystr + ' ' + logdestr + ' ' + iterstr + ' ' + avgfstr + ' ' + maxfstr + ' ' + atomstr + ' ' + volstr + ' ' + magstr + ' ' + timehrstr+ '\n')
                    parser_file_write.write('\n')
                else:
                    print(stepstr, energystr, logdestr, iterstr, avgfstr, maxfstr, atomstr, volstr, timehrstr)       
                    print('')
                    parser_file_write.write(str(stepstr + energystr + logdestr + iterstr + avgfstr + maxfstr + atomstr + volstr + timehrstr) + '\n') 
                    parser_file_write.write('\n')
                
        parser_file_write.close()
        
    # CREATING THE PLOTS THAT SHOW THE CONVERGENCE CRITERIA 
    if args.OUTPUT_SCF is True: 
        working_dir = os.path.join(DIR_, 'zz-OUTCAR-parse')
        if not os.path.exists(os.path.join(DIR_, 'zz-OUTCAR-parse')):
            os.makedirs(os.path.join(DIR_, 'zz-OUTCAR-parse'))

        for electronic_ in electronic_dict.keys():
            xlength = NELMAX 
            if electronic_ == 1:
                filename = 'conv-elec-step-' + str(electronic_).zfill(3) 
                plt.figure()
                plt.title('Convergence for ' + str(electronic_).zfill(3) + ' Electronic step')
                plt.scatter(electronic_dict[electronic_][SCF_KEY], electronic_dict[electronic_][DIFF_KEY])
                plt.plot(list(range(0,xlength)), np.full((xlength,1),EDIFF), color='red', linestyle='dashed')
                plt.annotate(xy=[xlength,EDIFF],s='EDIFF = 10^'+ str(EDIFF), xytext=(1,EDIFF*1.15))
                plt.annotate(s=str(electronic_dict[electronic_][SCF_KEY][-1]) + ' steps',
                             xy=[electronic_dict[electronic_][SCF_KEY][-1],electronic_dict[electronic_][DIFF_KEY][-1]],
                             xytext=[electronic_dict[electronic_][SCF_KEY][-1] + 10,float(electronic_dict[electronic_][DIFF_KEY][-1])*1.1])
                plt.axis([0, xlength, math.log10(1e-8), math.log10(1e6)])
                plt.xlabel('SCF Iteration #')
                plt.ylabel('Log|dE|')         
                plt.yticks(np.arange(math.log10(1e-8), math.log10(1e7), step = 2))
                plt.savefig(os.path.join(working_dir, filename) + '.png')
    
    
    if args.WRITE_FORCES is True: 
        FORCE_FILE = os.path.join(DIR_,'ab-FORCE-PARSE.txt')
        with open(FORCE_FILE,'w') as force_file:
            force_file.write('# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #' + '\n\n')
            force_file.write('                              Writing out force information!                       ' + '\n\n')           
            force_file.write('# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #' + '\n\n')
            for iteration in force_dict.keys():
                force_file.write('Iteration: ' + str(iteration).zfill(3) + '\n')
                force_file.write(' Average Force:' + str(round(force_dict[iteration][AVERAGE_FORCE], 4)).rjust(9) + '\n')
                force_file.write(' Maximum Force:' + str(round(force_dict[iteration][MAX_FORCE], 4)).rjust(9) + '\n')
                force_file.write('Max Force Atom:' + str(force_dict[iteration][MAX_ATOM]).rjust(9) + '\n\n')
                for a in range(0, len(force_dict[iteration][ATOM_COUNT])):
                    force_str = str(round(force_dict[iteration][ATOMS_FORCE_RAW][a][0],5)).rjust(11) + str(round(force_dict[iteration][ATOMS_FORCE_RAW][a][1],5)).rjust(11) + str(round(force_dict[iteration][ATOMS_FORCE_RAW][a][2],5)).rjust(11)  
                    max_str   = str(round(force_dict[iteration][MAGNITUDES][a],5)).rjust(11)
                    force_file.write(str(force_dict[iteration][ATOM_COUNT][a]).rjust(6) + force_str + max_str + '\n')
                force_file.write('\n')
    
        force_file.close()
        
            
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T 
    
if __name__ == '__main__':
        main()