#!/usr/bin/env python
#
# Stephen Patrick Vicchio
# 2019-02-27
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
# [structure.py] Provides information on the POSCAR to identify which flags
# should be frozen. T  

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
#  INPUT: POSCAR from VASP 
# OUTPUT: txt file similar to VASP POSCAR except contains atom name 
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# L I S T   O F   I M P O R T S 
import os 
import sys
import re 
import argparse

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   P A R A M E T E R S 

FAIL = '\033[91m'
ENDC = '\033[0m'
DIR_ = os.getcwd()
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   F U N C T I O N 


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# M A I N   P R O G R A M  

def main():
    # Parsing the command line arguments
    parser = argparse.ArgumentParser(description="""\nThis script is designd to
                                     compare the POSCAR and POTCAR files to
                                     quickly check that they match. The script
                                     just needs to be run in the directory
                                     containing both the POTCAR and POSCAR 
                                     files.""")
    parser.add_argument('-i', action='store', dest='POSCAR_FILE', default=None,
                        help='POSCAR file to read')
    parser.add_argument('-p', action='store', dest='POTCAR_FILE', default=None,
                        help='POTCAR file to read')
    args = parser.parse_args()
    
    
    if args.POSCAR_FILE is None: 
        readPOSCAR = os.path.join(DIR_, 'POSCAR')
    else:
        readPOSCAR = args.POSCAR_FILE
    
    if args.POTCAR_FILE is None:
        readPOTCAR = os.path.join(DIR_, 'POTCAR')
    else:
        readPOTCAR = args.POTCAR_FILE
    
    
    
    
    try: 
        POSCAR = open(readPOSCAR, "r")
        POTCAR = open(readPOTCAR, "r")
    except IOError:
        sys.stderr.write(FAIL)
        sys.stderr.write("\nThere was a problem reading either the POSCAR or POTCAR file.\n")
        sys.stderr.write(ENDC+"\n")
        sys.exit()
 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #       
# READING THE POTCAR AND POSCAR FILES 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #    
    
    # looking at the POTCAR file
    POTCARlines=POTCAR.readlines()
    re_potcar = re.compile('TITEL  = PAW_PBE')
    potcar_dict = {}
    count1 = 0 
    for line in POTCARlines:
        if re_potcar.search(line):
            count1 += 1
            potcar_dict[str(count1)] = line.split()[3].replace('_sv','')
    
    # looking at the POSCAR file 
    POSCARlines=POSCAR.readlines()    
    poscar_dict = {}
    count2 = 0 
    for i in range(0, len(POSCARlines)):
        if i == 5:
            for atom in POSCARlines[i].split():
                count2 +=1
                poscar_dict[str(count2)] = atom
        
    
    if len(potcar_dict.keys()) == len(poscar_dict.keys()):
        for order_key in potcar_dict.keys():
            if potcar_dict[order_key] == poscar_dict[order_key]:
                pass
            else:
                sys.stderr.write(FAIL)
                sys.stderr.write("""\nThe atoms DO NOT match.\n""")
                sys.stderr.write(ENDC+"\n")
                sys.exit()
    else: 
         sys.stderr.write(FAIL)
         sys.stderr.write("""\nThe atom counts do NOT match.\n""")
         sys.stderr.write(ENDC+"\n")
         sys.exit()
         
         
    print('\nEverything is looking good! The atoms in your POSCAR and POTCAR files match!\n')
                
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T 
    
if __name__ == '__main__':
        main()
