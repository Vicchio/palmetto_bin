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

def atom_index_creation(atom_string, atom_count): 
    
    dict_atom = {}
    list_atom_order = []
    freeze_dict = {}

    for catom in range(0, len(atom_string.split())):
        dict_atom[atom_string.split()[catom]] = atom_count.split()[catom]
    
    start = 0 
    for atom_key in dict_atom.keys():
        for i in range(start, int(dict_atom[atom_key]) + start):
            list_atom_order.append(str(atom_key).rjust(2) + '(' + str(i).zfill(3) + ')')
            freeze_dict[str(atom_key).rjust(2) + '(' + str(i).zfill(3) + ')'] = {}
            freeze_dict[str(atom_key).rjust(2) + '(' + str(i).zfill(3) + ')'][NUMBER] = str(i).zfill(3) 
            freeze_dict[str(atom_key).rjust(2) + '(' + str(i).zfill(3) + ')'][RELAX] = None
        start = i + 1
    
    return list_atom_order, freeze_dict

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# M A I N   P R O G R A M  

def main():
    # Parsing the command line arguments
    parser = argparse.ArgumentParser(description="""\nThis script is designed 
                                     to parse VASP outcar files to provide 
                                     information on how each run converged.""")
    parser.add_argument('-i', action='store', dest='OUTCAR_file', default="OUTCAR",
                        help='OUTCAR file to be parsed')
    parser.add_argument('-w', action='store', dest='OUTPUT_SCF', default=False,
                        help='set as True to generate SCF convergence files')
    parser.add_argument('-d', action='store', dest='STOP_DISPLAY', default=False,
                        help='set to True to stop display in terminal' )
    parser.add_argument('-forces', action='store', dest='WRITE_FORCES', default=False,
                        help='determines whether or not to write the forces')
    parser.add_argument('-stages', action='store', dest='', default=False,
                        help='')
    parser.add_argument('--version', action='version', version='%(prog)s 1.3.1')    
    args = parser.parse_args()
    
    if args.OUTPUT_SCF == 'True':
        args.OUTPUT_SCF = True 
    if args.STOP_DISPLAY == 'True':
        args.STOP_DISPLAY = True 
    if args.WRITE_FORCES == 'True':
       args.WRITE_FORCES = True  

    if os.path.isfile(args.OUTCAR_file) is True: 
        READFILE = args.OUTCAR_file
    try: 
        outcar = open(READFILE,"r")
    except IOError:
        sys.stderr.write(FAIL)
        sys.stderr.write("There was a problem opening the OUTCAR file. Does" /
                         "it exist at all?")
        sys.stderr.write(ENDC+"\n")
        sys.exit(1)

    if os.path.isfile('POSCAR') is True:
        POSCARFILE = 'POSCAR'
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
            for pcount in range(0, 11):            
                if pcount == 5:
                    atom_index = str(poscarlines[pcount])
                elif pcount == 6: 
                    atom_count = str(poscarlines[pcount])
                    list_atoms, freeze_status_dict = atom_index_creation(atom_index, atom_count)
                elif pcount == 9:
                    for z in range(0, len(freeze_status_dict.keys())):
                        a_status = poscarlines[pcount + z].split()[3]
                        b_status = poscarlines[pcount + z].split()[4]
                        c_status = poscarlines[pcount + z].split()[5]
                        if a_status is 'F' and b_status is 'F' and c_status is 'F':
                            freeze_status_dict[list_atoms[z]][RELAX] = False
                        else: 
                            freeze_status_dict[list_atoms[z]][RELAX] = True
        poscar_file.close()
       

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #       
# Starting to PARSE the OUTCAR file 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        
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
        re_energy_TOT = re.compile('  free  energy   TOTEN  = ')
        re_energy_sig = re.compile('  energy  without entropy=')
        re_end = re.compile('General timing and accounting informations for this job:')
        re_vasp_forces = re.compile('  FORCES: ')
        re_EDIFFG = re.compile('  EDIFFG =')
        re_FREE = re.compile(FREE_ENERGY_TOTEN)
        
        
        cputime_min = 0.0
        cputime_hrs = 0.0
        volume_val = None
        
        # List of starting variables
        magmom = None
        line_count = 0 
        electronic_count = 0 
        scf_count = 0 
        electronic_dict = {}
        force_dict = {}
        time_dict = {}
        volume_dict = {}
        spinpolarized = False
        FINISH_RUN_STATUS = False
        status_volume_change = False
        convergence_status = "UNCONVERGED"
        
        for line in outcarlines: 

            if re_EDIFFG.search(line):
                EDIFFG_VALUE = float(line.split()[2])
                if EDIFFG_VALUE > 0: 
                    ENERGY_CONV = True
                elif EDIFFG_VALUE < 0: 
                    ENERGY_CONV = False
            
            # Electronic optimization AND scf_count 
            if re_iteration.search(line):                
                electronic_count = int(line.split()[2][0:-1])                
                scf_count = int(line.split()[3][0:-1])
                cputime_min = 0.0
                cputime_hrs = 0.0 
                
                # Creates the flags to search OUTCAR File
                if electronic_count == 1: 
                    re_energy_scf = re.compile('free energy    TOTEN')
                    ENERGY_GRAB = 4
                else: 
                    re_energy_scf = re.compile('  free energy =')
                    ENERGY_GRAB = 3
                    
            # Computing Force Parameters
            if re_force.search(line):
                temp_force_magnitudes_list = []
                if electronic_count not in force_dict.keys():
                    # Generates the force dict 
                    force_dict[electronic_count] = {}
                    force_dict[electronic_count][ATOM_COUNT] = []
                    force_dict[electronic_count][ATOMS_FORCE_RAW] = []
                    force_dict[electronic_count][MAGNITUDES] = []
                    force_dict[electronic_count][CONVERT_RAW_FORCE] = []
                    force_dict[electronic_count][X_COORDS] = []
                    force_dict[electronic_count][Y_COORDS] = []
                    force_dict[electronic_count][Z_COORDS] = []
                    force_dict[electronic_count][X_FORCES] = []
                    force_dict[electronic_count][Y_FORCES] = []
                    force_dict[electronic_count][Z_FORCES] = []
                    force_dict[electronic_count][RELAX]    = []
                    force_dict[electronic_count][RMS_FORCE] = 0
                    
                for i in range(0,NATOMS):
                    force_dict[electronic_count][ATOM_COUNT].append(list_atoms[i])
                    raw_forces = outcarlines[line_count+i+2].split()
                    force_dict[electronic_count][X_COORDS].append(float(raw_forces[0]))
                    force_dict[electronic_count][Y_COORDS].append(float(raw_forces[1]))
                    force_dict[electronic_count][Z_COORDS].append(float(raw_forces[2]))
                    force_dict[electronic_count][X_FORCES].append(float(raw_forces[3]))
                    force_dict[electronic_count][Y_FORCES].append(float(raw_forces[4]))
                    force_dict[electronic_count][Z_FORCES].append(float(raw_forces[5]))
                    force_dict[electronic_count][MAGNITUDES].append(math.sqrt(math.pow(float(raw_forces[3]),2) + math.pow(float(raw_forces[4]),2) + math.pow(float(raw_forces[5]),2))) 
                    force_dict[electronic_count][RELAX].append(freeze_status_dict[list_atoms[i]][RELAX])
                    
                    if freeze_status_dict[list_atoms[i]][RELAX] is True: 
                        force_dict[electronic_count][RELAX].append(freeze_status_dict[list_atoms[i]][RELAX])
                        temp_force_magnitudes_list.append(math.sqrt(math.pow(float(raw_forces[3]),2) + math.pow(float(raw_forces[4]),2) + math.pow(float(raw_forces[5]),2)))     
                  
                # Computing the maximum forces
                force_dict[electronic_count][MAX_FORCE] = float(max(temp_force_magnitudes_list))
                force_dict[electronic_count][MAX_ATOM] = force_dict[electronic_count][ATOM_COUNT][force_dict[electronic_count][MAGNITUDES].index(max(temp_force_magnitudes_list))]    
                
            # Compute VASP Force Parameters
            if re_vasp_forces.search(line):
                force_dict[electronic_count][VASP_MAX_FORCE] = float(line.split()[4])
                force_dict[electronic_count][VASP_RMS_FORCE] = float(line.split()[5])
                                
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
                volume_dict[electronic_count] = float(line.split()[4])
                if len(volume_dict.keys()) == 1:
                    pass
                else:
                    if volume_dict[electronic_count] != volume_dict[electronic_count-1]:
                        status_volume_change = True 
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
                        
            
            if re_FREE.search(line):
                electronic_dict[electronic_count][FREE_ENERGY_TOTEN] = float(line.split()[4])                  
                
            # TOTEN FREE ENERGY VALUE     
            if re_energy_TOT.search(line):
                electronic_dict[electronic_count][TOTEN_ENERGY] = float(line.split()[4])
                
            # DISPERSION ENERGY VALUE                 
            if re_energy_dis.search(line):
                electronic_dict[electronic_count][DIS_ENERGY] = float(line.split()[2])
            
            # ENERGY(sigma->0) VALUE
            if re_energy_sig.search(line):
                electronic_dict[electronic_count][NO_ENTROPY_ENERGY] = float(line.split()[3])
                electronic_dict[electronic_count][SIGMA_ENERGY] = float(line.split()[6])
            
            # Checks to see if the end of the file is there
            if re_end.search(line):
                FINISH_RUN_STATUS = True
            
            line_count += 1 #IMPORTANT: required for finding 
            

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #       
# Printing out information and writing information to file 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    parser_file_write2 = open(os.path.join(DIR_, PARSER_FILE), 'w')
    parser_file_write2.write('\n')
  
    if FINISH_RUN_STATUS is True:      
        print('\n - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')  
        for step in electronic_dict.keys():
            stepstr   = str(str(step).zfill(2)).rjust(5)
#            energystr = "Energy: " + ("%3.6f" % (electronic_dict[step][ENERGY_KEY][-1])).rjust(12)
            energystr = "Energy: " + ("%3.6f" % (electronic_dict[step][FREE_ENERGY_TOTEN])).rjust(12)
            if step is 1: 
                diffE = 0
            else:     
                diffE = math.log10(abs(electronic_dict[step][FREE_ENERGY_TOTEN] - electronic_dict[step-1][FREE_ENERGY_TOTEN]))
                if ENERGY_CONV is True and diffE < math.log10(EDIFFG_VALUE):
                    convergence_status = "CONVERGED"
                elif ENERGY_CONV is False and abs(force_dict[step][VASP_MAX_FORCE]) <= abs(EDIFFG_VALUE): 
                    convergence_status = "CONVERGED"
            logdestr  = "Log|dE|: " + ("%1.3f" % (diffE)).rjust(6)					
            iterstr   = "SCF: " + ("%3i" % (electronic_dict[step][SCF_KEY][-1]))
            timehrstr   = "Time: " + ("%3.2fhr" % (time_dict[step]['hours'])).rjust(6)
            avgfstr = "RMS|F|: " + ("%2.4f" % (force_dict[step][VASP_RMS_FORCE])).rjust(6)
            maxfstr = "Max|F|: " + ("%2.4f" % (force_dict[step][VASP_MAX_FORCE])).rjust(6)
            atomstr = "Max Atom: " + str(force_dict[step][MAX_ATOM]).rjust(5)
            if status_volume_change is True: 
                volstr = "Vol.: " + ("%3.1f" % (volume_dict[step])).rjust(5)
                parser_file_write2.write(str(stepstr + ' ' + energystr + ' ' + logdestr + ' ' + iterstr + ' ' + avgfstr + ' ' + maxfstr + ' ' + atomstr+ ' '+ timehrstr) + '\n')
                print(stepstr, energystr, logdestr, iterstr, avgfstr, maxfstr, atomstr, volstr, timehrstr)
            else: 
                parser_file_write2.write(str(stepstr + ' ' + energystr + ' ' + logdestr + ' ' + iterstr + ' ' + avgfstr + ' ' + maxfstr + ' ' + atomstr  + ' ' + timehrstr) + '\n')
                print(stepstr, energystr, logdestr, iterstr, avgfstr, maxfstr, atomstr, timehrstr)
        
            converstr = str('Structural relaxation: ').rjust(23) + convergence_status + ' (' + str(step).zfill(2) + ' steps)'
            magstr    = str("MagMom: ").rjust(23) + ("%2.2f" % (magmom)).rjust(9)
            freeEstr  = str('Free Energy TOTEN: ').rjust(23) + ("%3.8f" % (electronic_dict[step][TOTEN_ENERGY]) + ' eV').rjust(18) 
            tsstr     = str('T*S: ').rjust(23) + ("%3.8f" % (electronic_dict[step][TOTEN_ENERGY] - electronic_dict[step][NO_ENTROPY_ENERGY]) + ' eV').rjust(18) 
            sigmastr  = str('Energy(sigma->0): ').rjust(23) + ("%3.8f" % (electronic_dict[step][SIGMA_ENERGY]) + ' eV').rjust(18) 
            

    elif FINISH_RUN_STATUS is False: 
        print('\n - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')  
        for step in electronic_dict.keys():
            if step < len(electronic_dict.keys())+1:
                stepstr   = str(str(step).zfill(2)).rjust(5)
#            energystr = "Energy: " + ("%3.6f" % (electronic_dict[step][ENERGY_KEY][-1])).rjust(12)
                energystr = "Energy: " + ("%3.6f" % (electronic_dict[step][ENERGY_KEY][-1])).rjust(12)
                if step is 1: 
                    diffE = 0
                else:     
                    energystr = "Energy: " + ("%3.6f" % (electronic_dict[step][FREE_ENERGY_TOTEN])).rjust(12)
                    diffE = math.log10(abs(electronic_dict[step][FREE_ENERGY_TOTEN] - electronic_dict[step-1][FREE_ENERGY_TOTEN]))
                    if ENERGY_CONV is True and diffE < math.log10(EDIFFG_VALUE):
                        convergence_status = "CONVERGED"
                    elif ENERGY_CONV is False and abs(force_dict[step][VASP_MAX_FORCE]) <= abs(EDIFFG_VALUE): 
                        convergence_status = "CONVERGED"
                logdestr  = "Log|dE|: " + ("%1.3f" % (diffE)).rjust(6)					
                iterstr   = "SCF: " + ("%3i" % (electronic_dict[step][SCF_KEY][-1]))
                timehrstr   = "Time: " + ("%3.2fhr" % (time_dict[step]['hours'])).rjust(6)
                if len(electronic_dict.keys()) == 1:
                    avgfstr = "RMS|F|: " + str('None').rjust(6)
                    maxfstr = "Max|F|: " + str('None').rjust(6)
                    atomstr = "Max Atom: " + str('None').rjust(5)    
                else:
                    avgfstr = "RMS|F|: " + ("%2.4f" % (force_dict[step][VASP_RMS_FORCE])).rjust(6)
                    maxfstr = "Max|F|: " + ("%2.4f" % (force_dict[step][VASP_MAX_FORCE])).rjust(6)
                    atomstr = "Max Atom: " + str(force_dict[step][MAX_ATOM]).rjust(5)
                if status_volume_change is True: 
                    volstr = "Vol.: " + ("%3.1f" % (volume_dict[step])).rjust(5)
                    parser_file_write2.write(str(stepstr + ' ' + energystr + ' ' + logdestr + ' ' + iterstr + ' ' + avgfstr + ' ' + maxfstr + ' ' + atomstr+ ' '+ timehrstr) + '\n')
                    print(stepstr, energystr, logdestr, iterstr, avgfstr, maxfstr, atomstr, volstr, timehrstr)
                else: 
                    parser_file_write2.write(str(stepstr + ' ' + energystr + ' ' + logdestr + ' ' + iterstr + ' ' + avgfstr + ' ' + maxfstr + ' ' + atomstr  + ' ' + timehrstr) + '\n')
                    print(stepstr, energystr, logdestr, iterstr, avgfstr, maxfstr, atomstr, timehrstr)
                
                converstr = str('Structural relaxation: ').rjust(23) + convergence_status + ' (' + str(step).zfill(2) + ' steps)'
                magstr    = str("MagMom: ").rjust(23) + ("%2.2f" % (magmom)).rjust(9)
                if len(electronic_dict.keys()) == 1:
                    freeEstr  = str('Free Energy TOTEN: ').rjust(23) + str('None' + ' eV').rjust(6) 
                    tsstr     = str('T*S: ').rjust(23) + str('None' + ' eV').rjust(6) 
                    sigmastr  = str('Energy(sigma->0): ').rjust(23) + str('None' + ' eV').rjust(6)
                else:
                    freeEstr  = str('Free Energy TOTEN: ').rjust(23) + ("%3.8f" % (electronic_dict[step][TOTEN_ENERGY]) + ' eV').rjust(18) 
                    tsstr     = str('T*S: ').rjust(23) + ("%3.8f" % (electronic_dict[step][TOTEN_ENERGY] - electronic_dict[step][NO_ENTROPY_ENERGY]) + ' eV').rjust(18) 
                    sigmastr  = str('Energy(sigma->0): ').rjust(23) + ("%3.8f" % (electronic_dict[step][SIGMA_ENERGY]) + ' eV').rjust(18) 
            
    parser_file_write2.write('\n - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n\n')
    parser_file_write2.write(converstr + '\n')
    parser_file_write2.write(magstr + '\n')
    parser_file_write2.write(freeEstr + '\n')
    parser_file_write2.write(tsstr + '\n')
    parser_file_write2.write(sigmastr + '\n')
    parser_file_write2.write('\n')

    print('\n - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')
    print(converstr)
    print(magstr)
    print(freeEstr)
    print(tsstr)
    print(sigmastr)
    print('')
    
    parser_file_write2.close()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #       
# Creating the plot for the first stage SCF convergence 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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
    
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #       
# Writing the forces for each step into a text file for easy access
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #    

    if args.WRITE_FORCES is True: 
        FORCE_FILE = os.path.join(DIR_,'ab-FORCE-PARSE.txt')
        with open(FORCE_FILE,'w') as force_file:
            force_file.write('# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #' + '\n\n')
            force_file.write('                              Writing out force information!                       ' + '\n\n')           
            force_file.write('# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #' + '\n\n')
            for iteration in force_dict.keys():
                force_file.write('     Iteration:' + str(iteration).zfill(3).rjust(10) + '\n')
                force_file.write('     RMS Force:' + str(round(force_dict[iteration][VASP_RMS_FORCE], 5)).rjust(10) + '\n')
                force_file.write(' Maximum Force:' + str(round(force_dict[iteration][MAX_FORCE], 5)).rjust(10) + '\n')
                force_file.write('Max Force Atom:' + str(force_dict[iteration][MAX_ATOM]).rjust(10) + '\n\n')
                force_file.write(str('VMD Index').rjust(10) + '  |  ' + str('Coords (x, y, z)').center(27) + '  |  ' + str('Forces (Fx, Fy, Fz)').center(27) + '  |  ' + str('Magnitude').center(10) + '\n')
                for a in range(0, len(force_dict[iteration][ATOM_COUNT])):
                    atom_str = str(force_dict[iteration][ATOM_COUNT][a]).rjust(10)
                    x1_str   = ("%2.4f" % (force_dict[iteration][X_COORDS][a])).rjust(7)
                    y1_str   = ("%2.4f" % (force_dict[iteration][Y_COORDS][a])).rjust(7)
                    z1_str   = ("%2.4f" % (force_dict[iteration][Z_COORDS][a])).rjust(7)
                    xf_str   = ("%2.4f" % (force_dict[iteration][X_FORCES][a])).rjust(7)
                    yf_str   = ("%2.4f" % (force_dict[iteration][Y_FORCES][a])).rjust(7)
                    zf_str   = ("%2.4f" % (force_dict[iteration][Z_FORCES][a])).rjust(7)
                    mag_str  = ("%2.4f" % (force_dict[iteration][MAGNITUDES][a])).rjust(7) 
                    force_file.write(atom_str + '  |  ' + x1_str + '   ' + y1_str + '   ' + z1_str + '  |  ' + xf_str + '   ' + yf_str + '   ' + zf_str + '  |  ' + mag_str + '\n')
                force_file.write('\n\n# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #' + '\n\n')
            
        force_file.close()
        
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T 
    
if __name__ == '__main__':
        main()