#!/usr/bin/env python
# 
# Stephen Patrick Vicchio 
# 2019-01-18
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Removes specific atoms from the POSCAR file and reformats
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
#  INPUT: POSCAR file with atom (index) to be removed)
# OUTPUT: POSCAR file with the removed atoms AND the original POSCAR  
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  

import sys
import os
from itertools import groupby
import numpy as np

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def main():
	
	temp_file = 'POSCAR.temp'
	filepath = sys.argv[1]
	remove_atoms = sys.argv[2:]
	remove_atoms_dict = argv_remove_atoms_information(remove_atoms)
	
	if not os.path.isfile(filepath):
		print("File path {} does not exist. Exiting...".format(filepath))
		sys.exit()
	
	with open(filepath, 'r') as f_read, open(temp_file, 'w') as f_temp:
		cnt = 1
		for line in f_read:
			if cnt == 1:
				first_atoms = create_atom_counts(line)
			elif cnt == 6:
				sixth_atoms = create_atom_counts(line)
			elif cnt == 7: 
				atom_count = create_atom_counts(line) 
				atoms_dict = create_atom_dictionary(first_atoms, sixth_atoms, atom_count)
				edit_atoms_dict = edit_atom_count(atoms_dict, remove_atoms_dict) 	
				new_atoms, new_count = new_atoms_count(edit_atoms_dict)
				index_list = create_atoms_list(atoms_dict)
			# WRITING ALL THE INFORMATION INTO NEW OUTPUT FILE	
			if cnt <= 5:
				f_temp.write(line)
			elif cnt == 6:
				# the information from line 6 (atoms order) is written  
				# when line 7 (below) is added 
				pass
				#f_temp.write(new_atoms)
			elif cnt == 7:
				f_temp.write(new_atoms)
				f_temp.write(new_count)
				org_count = total_atoms(atoms_dict)
				map_atoms(edit_atoms_dict)
				map_atoms(atoms_dict)
			elif cnt == 8: 
				f_temp.write(line)				
#				f_temp.write('Direct\n')
#				f_temp.write('Selective dynamics\n')
			elif cnt >= 8 and cnt<= org_count + 8: 
				current_structure = index_list[cnt - 9]
#				print(cnt, current_structure) 
				if current_structure in remove_atoms:
#					print(cnt, cnt-8, current_structure, 'SKIP')
					pass
				elif current_structure not in remove_atoms:
#					print(cnt, cnt-8 ,current_structure, line)
					f_temp.write(line)
			cnt += 1
	
	f_read.close()
	f_temp.close()
	
	os.rename('POSCAR', 'POSCAR-org')
	os.rename(temp_file, 'POSCAR')
	
	return 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def create_atoms_list(atoms_dict):
	total = total_atoms(atoms_dict)
	index_list = []
	for key in atoms_dict.keys():
		temp_list = []
		for i in range(1, atoms_dict[key] + 1):
			temp_list.append(str(key) + str(i))	
		index_list.extend(temp_list)
	
	if total != len(index_list):
		print('\n \n WARNING: There is a mismatch in index lengths. ({} /= {})\n \n'.format(total, len(index_list)))
		sys.exit	
	else:
		pass	
	return index_list

def map_atoms(atoms_dict):
	count = 0
	new_dict = {} 
	for keys in atoms_dict.keys():
		count += atoms_dict[keys]
		new_dict[keys] = count 	
	
#	print(new_dict)
	return 

def total_atoms(atoms_count):
	total = 0 
	for keys in atoms_count.keys():
		total += atoms_count[keys]	
#	print(atoms_count)
		
#	print(total)
	return total

def new_atoms_count(edit_atom_dict): 
	atoms_list = []
	count_list = []
	for key in edit_atom_dict.keys():
		atoms_list.append(key)
		count_list.append(str(edit_atom_dict[key]))
	new_line_atoms = "  ".join(atoms_list) + '\n'
	new_line_count = " ".join(count_list) + '\n'	
	return new_line_atoms, new_line_count

def edit_atom_count(atoms_dict, remove_atoms_dict):
	edit_atom_dict = {}	
	for key in atoms_dict.keys():
		if key in remove_atoms_dict.keys():
			edit_atom_dict[key] = atoms_dict[key] - int(len(remove_atoms_dict[key]))	
		else:
			edit_atom_dict[key] = atoms_dict[key]
	return edit_atom_dict 


def split_text(s):
	split = []
	for k,g in groupby(s, str.isalpha):
		split_temp = ''.join(list(g))
		split.append(split_temp)
	return split

def argv_remove_atoms_information(list_atoms_remove):
	dict_atoms_remove = {}
	for atom in list_atoms_remove:
		atom_split = split_text(atom)
		if atom_split[0] not in dict_atoms_remove.keys():
			dict_atoms_remove[atom_split[0]] = []
		dict_atoms_remove[atom_split[0]].append(atom_split[1])
	return dict_atoms_remove 

def create_atom_dictionary(first_atoms, second_atoms, atom_count):
	if first_atoms == second_atoms:
		atoms_dict = {}
		for i in range(len(atom_count)):
			atoms_dict[first_atoms[i]] = int(atom_count[i])		
	else:
		print('\n \n WARNING: The 1st and 7th line DO NOT match. \n \n')
		sys.exit
	return(atoms_dict) 

def create_atom_counts(line_atoms):
	list_atoms = line_atoms.split()
	return(list_atoms)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if __name__ == '__main__':
	main()


