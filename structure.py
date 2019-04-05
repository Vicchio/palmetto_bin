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
import subprocess 
import os 
import sys
import math
import numpy as np 
import re 
import argparse
import shutil 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   P A R A M E T E R S 

FAIL = '\033[91m'
ENDC = '\033[0m'

DIR_ = os.getcwd()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# L I S T   O F   F U N C T I O N 

def list_of_atoms(top_buffer,dict_):
    """
    INPUT the buffer number of lines at the top of the POSCAR file and a 
    dictionary containing keys as atoms and values as the number of those atoms
    in the system. The OUTPUT is a list containing the order of the atoms in 
    your system to help determine what atoms should be frozen and which should 
    be allowed to relax. 
    
    [INPUTS]
    (1) top_buffer - the number of lines before the coordinates begin in POSCAR
    (2) dict_      - dictionary containing the information about system atoms
    
    [OUTPUTS]
    (1) list_of_atoms - list containing all the atoms in the system (IN ORDER)
    """
    
    list_of_atoms = []
    
    for x in range(0,top_buffer+1):
        list_of_atoms.append('SKIP')
    
    for key, val in dict_.items():
        for j in range(1,val+1):
            list_of_atoms.append(str(key)+str(j).zfill(3))
    
    return list_of_atoms



def remove_new_line(list_):
    """
    Removes the '\n' that is located at the end of the python line when loading
    the atoms into script 
    
    [INPUT]
    (1) string that contains '\n'
    
    [OUTPUT]
    (1) the INPUT string without the '\n'
    """
    new_list = []
    
    for val in list_:
        new_list.append(val.strip())
    
    return new_list 

def flip_flags(str_):
    """
    Flips the strings associated with a specific atom
    
    [INPUT]
    (1) the current string for the structure
    
    [OUTPUT]
    (2) the 'flipped' string for the structure 
    """
    if str_ == 'T':
        new_str = 'F'
    elif str_ == 'F':
        new_str = 'T'
    
    return new_str

def distance_formula(x1, y1, z1, x2, y2, z2):
    """
    Computes the distance between the points (x1, y1, z1) and (x2, y2, z2)
    
    [INPUTS]
    (1) (x1, y1, z1) and (x2, y2, z2) are cartesian coordinates
    
    [OUTPUTS]
    (2) the distance between the points
    """
    diff_x = (float(x1) - float(x2))
    diff_y = (float(y1) - float(y2))
    diff_z = (float(z1) - float(z2))
    
    distance = math.sqrt(diff_x*diff_x + diff_y*diff_y + diff_z*diff_z)
    
    return distance


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# M A I N   P R O G R A M  

def main():
    # Parsing the command line arguments
    parser = argparse.ArgumentParser(description="""\nThis script is designed
                                     to freeze certain structures in the POSCAR
                                     file based off the distance to a specific 
                                     atom. The user has control over both the 
                                     atom specified and the distance criteria.
                                     Please note that current the script ONLY
                                     works for FRACTIONAL coordinates.""")
    parser.add_argument('-i', action='store', dest='POSCAR_file', default="POSCAR",
                        help='POSCAR file to be parsed to reveal structure info')
    parser.add_argument('-r', action='store', dest='Reciprocal', default=None,
                        help='Atom string to determine which atoms are frozen \
                        and which atoms are freeze to relax')
    parser.add_argument('-d', action='store', dest='DISTANCE', default=None,
                        help='Distance in A to determine frozen atoms')
    parser.add_argument('-w', action='store', dest='OUTPUT_SCF', default=False,
                        help='set as True to generate SCF convergence files')
    parser.add_argument('-e', action='store', dest='EDIT_ATOMS', default=None,
                        help='list of atoms to flip T or F flag in POSCAR')
    parser.add_argument('--version', action='version', version='%(prog)s 1.1.1')    
    args = parser.parse_args()
    
    try:
        poscar_file = os.path.join(DIR_, args.POSCAR_file,"r")
        POSCAR = open(poscar_file,"r")
#        MOD_POSCAR_STATUS = os.path.isfile(os.path.join(os.getcwd(), 'POSCAR-modified.temp'))
        POSCAR.close()
    except IOError:
        sys.stderr.write(FAIL)
        sys.stderr.write("There was a problem opening the POSCAR file. Does" /
                         "it exist at all?")
        sys.stderr.write(ENDC+"\n")
        sys.exit()
 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #       
# Creating the modified POSCAR file
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #    


    # Checking to see whether or not a modified POSCAR file exists or not
    MOD_POSCAR_STATUS = os.path.isfile(os.path.join(os.getcwd(), 'POSCAR-modified.temp'))
        
    if POSCAR != None and MOD_POSCAR_STATUS is False:
        print('\nThere exists an POSCAR file!\n')
        
        # Opening all POSCAR file and reading all the lines 
        POSCAR = open(poscar_file, "r")
        POSCARlines = POSCAR.readlines()
        POSCAR.close()
        
        # Seatching the POSCAR file for when the coordinate line for 'Direct' starts
        SEARCH_='Direct'
        coordinate_line = int(str(subprocess.check_output(['grep', '-n', SEARCH_, poscar_file])).split('\'')[1].split(':')[0])-1
                             
        # Starting to create the modified POSCAR file 
        atoms_dict = {}                   
        with open(os.path.join(os.getcwd(), 'POSCAR-modified.temp'), 'w') as MOD_POSCAR:
            
            # Checks if there's a text file that contains the adopts to modify 
            if args.EDIT_ATOMS is not None: 
                with open(os.path.join(os.getcwd(), args.EDIT_ATOMS), 'r') as EDIT_ATOMS:
                    edit_atoms = EDIT_ATOMS.readlines()
                    EDIT_ATOMS.close()
                edit_atoms = remove_new_line(edit_atoms)
            
            # Adding the atom identifies to the beginning of the modified POSCAR
            for line in range(0,len(POSCARlines)-1):
                if line < coordinate_line:
                    if line == 5:
                        for atom in POSCARlines[line].split():
                            atoms_dict[atom] = None
                    elif line == 6:
                        atom_keys = atoms_dict.keys()
                        count = 0 
                        for atom_add in atom_keys:
                            atoms_dict[atom_add] = int(POSCARlines[line].split()[count])
                            count += 1  
                        atom_list = list_of_atoms(coordinate_line, atoms_dict)
                        print(atoms_dict)
                    MOD_POSCAR.write(POSCARlines[line])
#                    MOD_POSCAR.write(' SKIP $$$ ' + POSCARlines[line])
                elif line == coordinate_line:
                    MOD_POSCAR.write(POSCARlines[line])
#                    MOD_POSCAR.write(' SKIP $$$ ' + POSCARlines[line])
                elif line > coordinate_line:
                    atom     = str('# ' + atom_list[line]).rjust(8)
                    xcstr = str(POSCARlines[line].split()[0]).rjust(19)
                    ycstr = str(POSCARlines[line].split()[1]).rjust(20)
                    zcstr = str(POSCARlines[line].split()[2]).rjust(20)
          
                    # Section to flip flags for a few atoms based off text file
                    x_flags  = str(POSCARlines[line].split()[3])
                    y_flags  = str(POSCARlines[line].split()[4])
                    z_flags  = str(POSCARlines[line].split()[5])
                    if args.EDIT_ATOMS is not None: 
                        if atom_list[line] in edit_atoms:
                            x_flags = flip_flags(x_flags)
                            y_flags = flip_flags(y_flags)
                            z_flags = flip_flags(z_flags)
                    xfstr = str(x_flags).rjust(3)
                    yfstr = str(y_flags).rjust(3)
                    zfstr = str(z_flags).rjust(3)
                    MOD_POSCAR.write(xcstr +  ycstr + zcstr + xfstr + yfstr + zfstr + atom +'\n')
#                    MOD_POSCAR.write(atom +  xcstr +  ycstr + zcstr + xfstr + yfstr + zfstr + '\n')
            MOD_POSCAR.write('\n')
            MOD_POSCAR.close()
    elif POSCAR != None and MOD_POSCAR_STATUS is True and args.Reciprocal == None:
        sys.stderr.write(FAIL)
        sys.stderr.write('\nThere already exists a modified POSCAR!\n')
        sys.stderr.write(ENDC+"\n")
        sys.exit()
     
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #       
# Generating the relaxed- and frozen- POSCAR files 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
                
    if args.Reciprocal != None and MOD_POSCAR_STATUS is True:
        print('\nLet\'s now generate the relaxed- and frozen- POSCARs!\n')
        # Make a directory to store the updated files
        new_working_path = os.path.join(os.getcwd(), '00-POSCAR-mods')
        if not os.path.exists(new_working_path):
            os.makedirs(new_working_path)
        
        list_atoms_freeze = []
        list_atoms_relax = []
        dict_freeze = {}
        dict_relax = {}
        
        # Error message if you are trying to create relaxed- and frozen- POSCARs
        # but do NOT specify the distance on which you want to freeze or relax
        # atoms 
        if args.DISTANCE == None:
            sys.stderr.write(FAIL)
            sys.stderr.write('\nYOU ARE MISSING THE -d FLAG TO SET THE DISTANCE CRITERA!!\n')
            sys.stderr.write(ENDC+"\n")       
            sys.exit()
        elif args.DISTANCE != None: 
    
            # Collecting all the information from the modified POSCAR file
            with open(os.path.join(os.getcwd(), 'POSCAR-modified.temp'), 'r') as MOD_POSCAR:
                MODPOSCARlines = MOD_POSCAR.readlines()
                MOD_POSCAR.close()
                
            # Finding the coordinates to the atom that all other atoms will be 
            # compared to 
            found_atom_status = False
            re_central_atom = re.compile(str(args.Reciprocal))
            while found_atom_status is False:
                for reline in range(0,len(MODPOSCARlines)-1):
                    if re_central_atom.search(MODPOSCARlines[reline]):
                        # Creating the 3 by 1 array that contains the (x, y, z) coordiantes
                        fract_set_array = np.array([[float(MODPOSCARlines[reline].split()[2])],
                                                    [float(MODPOSCARlines[reline].split()[3])],
                                                    [float(MODPOSCARlines[reline].split()[4])]])
                        found_atom_status = True
                        
            for mline in range(0,len(MODPOSCARlines)-1):
                if MODPOSCARlines[mline].split()[0] == 'SKIP':
                    if mline == 1:
                        SCALING_FACTOR = float(MODPOSCARlines[mline].split()[2])
                    elif mline == 2:
                        ax = float(MODPOSCARlines[mline].split()[2]) * SCALING_FACTOR
                        ay = float(MODPOSCARlines[mline].split()[3]) * SCALING_FACTOR
                        az = float(MODPOSCARlines[mline].split()[4]) * SCALING_FACTOR
                    elif mline == 3:
                        bx = float(MODPOSCARlines[mline].split()[2]) * SCALING_FACTOR
                        by = float(MODPOSCARlines[mline].split()[3]) * SCALING_FACTOR
                        bz = float(MODPOSCARlines[mline].split()[4]) * SCALING_FACTOR
                    elif mline == 4: 
                        cx = float(MODPOSCARlines[mline].split()[2]) * SCALING_FACTOR
                        cy = float(MODPOSCARlines[mline].split()[3]) * SCALING_FACTOR
                        cz = float(MODPOSCARlines[mline].split()[4]) * SCALING_FACTOR
                    elif mline == 5:
                        for atom in MODPOSCARlines[mline].split()[2:]:
                            dict_freeze[atom] = 0
                            dict_relax[atom] = 0
                    elif mline == 6:
                        convert_M = np.array([[ax, ay, az], 
                                              [bx, by, bz],
                                              [cx, cy, cz]])
                        
                        cart_set_array = np.dot(np.transpose(convert_M), fract_set_array)   
                        
                        x_coord_set = cart_set_array[0]
                        y_coord_set = cart_set_array[1]
                        z_coord_set = cart_set_array[2]
                
                else:
                    x_coord_frac = float(MODPOSCARlines[mline].split()[2])
                    y_coord_frac = float(MODPOSCARlines[mline].split()[3])
                    z_coord_frac = float(MODPOSCARlines[mline].split()[4])
                    
                    fractional_array = np.array([[x_coord_frac],
                                                 [y_coord_frac],
                                                 [z_coord_frac]])

                    cart_array = np.dot(np.transpose(convert_M),
                                              fractional_array)
                    
                    x_coord_com = cart_array[0]
                    y_coord_com = cart_array[1]
                    z_coord_com = cart_array[2]
                
                    distance = distance_formula(x_coord_set, y_coord_set,
                                                z_coord_set, x_coord_com,
                                                y_coord_com, z_coord_com)
                    if distance > float(args.DISTANCE):
                        list_atoms_freeze.append(MODPOSCARlines[mline].split()[0])                       
                        dict_freeze[str(MODPOSCARlines[mline].split()[0][:-3])] += 1
                    elif distance <= float(args.DISTANCE):
                        list_atoms_relax.append(MODPOSCARlines[mline].split()[0])
                        dict_relax[str(MODPOSCARlines[mline].split()[0][:-3])] += 1
        
        
            
            # GENERATING THE NEW POSCAR FILE FOR MANIPULATION
                        
            SEARCH_='Direct'
            coordinate_line = int(str(subprocess.check_output(['grep', '-n', SEARCH_, args.POSCAR_file])).split('\'')[1].split(':')[0])-1
        
            with open(os.path.join(new_working_path, 'POSCAR-relax.temp'), 'w') as RELAX_POSCAR, \
            open(os.path.join(new_working_path, 'POSCAR-freeze.temp'), 'w') as FREEZE_POSCAR, \
            open(os.path.join(os.getcwd(), 'POSCAR-updated'), 'w') as UPDATED_POSCAR:
                for aline in range(0,len(MODPOSCARlines)-1):
                    if aline <= coordinate_line:
                        if aline < 5 or aline > 6:
                            RELAX_POSCAR.write(MODPOSCARlines[aline][10:])
                            FREEZE_POSCAR.write(MODPOSCARlines[aline][10:])
                            UPDATED_POSCAR.write(MODPOSCARlines[aline][10:])
                        elif aline ==5: 
                            UPDATED_POSCAR.write(MODPOSCARlines[aline][10:])
                        elif aline == 6:
                            relax_string = []
                            relax_string_num = []
                            for key_r in dict_relax.keys():
                                if dict_relax[key_r] != 0: 
                                    relax_string.append(str(key_r).rjust(4))
                                    relax_string_num.append(str(dict_relax[key_r]).rjust(4))
                            relax_string.append('\n')
                            relax_string_num.append('\n')
                            RELAX_POSCAR.write(''.join(relax_string))
                            RELAX_POSCAR.write(''.join(relax_string_num))
                            
                            freeze_string = []
                            freeze_string_num = []
                            for key_f in dict_freeze.keys():
                                if dict_freeze[key_f] != 0: 
                                    freeze_string.append(str(key_f).rjust(4))
                                    freeze_string_num.append(str(dict_freeze[key_f]).rjust(4))
                            freeze_string.append('\n')
                            freeze_string_num.append('\n')
                            FREEZE_POSCAR.write(''.join(freeze_string))
                            FREEZE_POSCAR.write(''.join(freeze_string_num))
                            UPDATED_POSCAR.write(MODPOSCARlines[aline][10:])
                    else:
                        xcstr_write = str(MODPOSCARlines[aline].split()[2]).rjust(19)
                        ycstr_write = str(MODPOSCARlines[aline].split()[3]).rjust(20)
                        zcstr_write = str(MODPOSCARlines[aline].split()[4]).rjust(20)
                        count = 0
                        if MODPOSCARlines[aline].split()[0] in list_atoms_freeze:
                            count += 1
                            freeze_flags = '  F  F  F'
                            FREEZE_POSCAR.write(xcstr_write + ycstr_write + zcstr_write + freeze_flags + '\n')
                            UPDATED_POSCAR.write(xcstr_write + ycstr_write + zcstr_write + freeze_flags + '\n')
                        elif MODPOSCARlines[aline].split()[0] in list_atoms_relax:
                            relax_flags = '  T  T  T'
                            RELAX_POSCAR.write(xcstr_write + ycstr_write + zcstr_write + relax_flags + '\n')
                            UPDATED_POSCAR.write(xcstr_write + ycstr_write + zcstr_write + relax_flags + '\n')
            
                UPDATED_POSCAR.write('\n')
            RELAX_POSCAR.close()
            FREEZE_POSCAR.close()
            UPDATED_POSCAR.close()
            
            shutil.copy(os.path.join(os.getcwd(), 'POSCAR-modified.temp'), os.path.join(new_working_path, 'POSCAR-modified.temp'))
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# R U N N I N G   S C R I P T 
    
if __name__ == '__main__':
        main()
