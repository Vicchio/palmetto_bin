#!/usr/bin/env bash
#
# Stephen Patrick Vicchio
# 2019-10-06
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 
# accepts a list of atoms to remove  
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  
# Here are the instructions for running the following script: 
# 
#       cp2k-remove_atoms.sh input.txt remove.txt
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

input_file=$1
atom_list_remove=remove-atoms.txt

if [[ -e ${atom_list_remove} ]]; then 
	#if there are atoms to delete...
	cp ${input_file} ${input_file}-modified

	declare -a COPY_LIST
	mapfile -t COPY_LIST < ${atom_list_remove}

	head -2 ${input_file%.*}.xyz > ${input_file%.*}-atoms-removed.xyz  

	for i in "${COPY_LIST[@]}"; do
		sed -i "/${i}/d" ${input_file}-modified
		grep "${i}" ${input_file%.*}.xyz >> ${input_file%.*}-atoms-removed.xyz
		sed -i "/${i}/d" ${input_file%.*}.xyz  
	done

	sed -i 's/#VMD.*//' ${input_file}-modified

	number_atoms_remove=$(wc -l < ${atom_list_remove} )
	number_of_atoms=$(grep "NUMBER_OF_ATOMS" ${input_file}-modified )
	number_of_atoms_number=$(tr -dc '0-9'<<< ${number_of_atoms})
	new_atoms_count=$((${number_of_atoms_number}-${number_atoms_remove}))

	sed -i "s/${number_of_atoms}/       NUMBER_OF_ATOMS ${new_atoms_count}/g" ${input_file}-modified

	sed -i "s/${number_of_atoms_number}/${number_atoms_remove}/g" ${input_file%.*}-atoms-removed.xyz
	sed -i "s/${number_of_atoms_number}/${new_atoms_count}/g" ${input_file%.*}.xyz  


	cp ${input_file} ${input_file}-origin
	cp ${input_file}-modified ${input_file} 
	
	mkdir 00-OUTPUT 01-VIS

	mv *xyz 01-VIS/. 
	mv *inp* 00-OUTPUT/.
	mv 00-OUTPUT/${input_file} .
else
	# if there are not atoms to delete.. then delete the VMD string information
	cp ${input_file} ${input_file}-modified
	sed -i 's/#VMD.*//' ${input_file}-modified
	cp ${input_file} ${input_file}-origin
	cp ${input_file}-modified ${input_file} 

        mkdir 00-OUTPUT 01-VIS

	mv *xyz 01-VIS/. 
	mv *inp* 00-OUTPUT/.
	mv 00-OUTPUT/${input_file} . 
fi


 
