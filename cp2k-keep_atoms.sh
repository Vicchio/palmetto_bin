#!/usr/bin/env bash
#
# Stephen Patrick Vicchio
# 2020-01-014
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 
# Accepts a list of atoms to keep   
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  
# Here are the instructions for running the following script: 
# 
#       cp2k-keep_atoms.sh input.inp #
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

input_file=$1
number_of_sites=$2
atom_list_remove=remove-atoms.txt
all_atoms_list=all-atoms.txt

if [[ -e ${atom_list_remove} && -e ${all_atoms_list} && -n ${number_of_sites} ]]; then 

	# Looking up directory information
	DIR=$(pwd)
	DIR_1UP="$(dirname "${DIR}")"
	BASE_1UP="$(basename "${DIR_1UP}")"
	DIR_2UP="$(dirname "${DIR_1UP}")"
	BASE_2UP="$(basename "${DIR_2UP}")"
	
	# Determining the site information	
	if [[ "${number_of_sites}" -eq "2" ]]; then 
		# Identifying the two sites
		site1_full=$(echo ${BASE_2UP} | cut -c 4-6)
		site2_full=$(echo ${BASE_2UP} | cut -c 8-10)
		site_file_info=$(echo ${BASE_2UP} | cut -c 4-10)
		
		# Collecting and deleting the site information 
		site1=$(grep -w "${site1_full}" ${all_atoms_list} | cut -c 5-11 ) 
		site2=$(grep -w "${site2_full}" ${all_atoms_list} | cut -c 5-11 )  
		sed -i "/${site1}/d" ${atom_list_remove}
		sed -i "/${site2}/d" ${atom_list_remove}
	elif [[ "${number_of_sites}" -eq "4" ]]; then 
		# Identifying the four sites
		site1_full=$(echo ${BASE_2UP} | cut -c 4-6)
		site2_full=$(echo ${BASE_2UP} | cut -c 8-10)
		site3_full=$(echo ${BASE_2UP} | cut -c 12-14)
		site4_full=$(echo ${BASE_2UP} | cut -c 16-18)
		site_file_info=$(echo ${BASE_2UP} | cut -c 4-18)
	
		# Collecting and deleting the site information 
		site1=$(grep -w "${site1_full}" ${all_atoms_list} | cut -c 5-11 ) 
		site2=$(grep -w "${site2_full}" ${all_atoms_list} | cut -c 5-11 )  
		site3=$(grep -w "${site3_full}" ${all_atoms_list} | cut -c 5-11 ) 
		site4=$(grep -w "${site4_full}" ${all_atoms_list} | cut -c 5-11 )  
		sed -i "/${site1}/d" ${atom_list_remove}
		sed -i "/${site2}/d" ${atom_list_remove}
		sed -i "/${site3}/d" ${atom_list_remove}
		sed -i "/${site4}/d" ${atom_list_remove}

	elif [[ "${number_of_sites}" -eq "6" ]]; then 
		# Identifying the six sites
		site1_full=$(echo ${BASE_2UP} | cut -c 4-6)
		site2_full=$(echo ${BASE_2UP} | cut -c 8-10)
		site3_full=$(echo ${BASE_2UP} | cut -c 12-14)
		site4_full=$(echo ${BASE_2UP} | cut -c 16-18)
		site5_full=$(echo ${BASE_2UP} | cut -c 20-22)
		site6_full=$(echo ${BASE_2UP} | cut -c 24-26)
		site_file_info=$(echo ${BASE_2UP} | cut -c 4-26)
		
		# Collecting and deleting the site information 
		site1=$(grep -w "${site1_full}" ${all_atoms_list} | cut -c 5-11 ) 
		site2=$(grep -w "${site2_full}" ${all_atoms_list} | cut -c 5-11 ) 
 		site3=$(grep -w "${site3_full}" ${all_atoms_list} | cut -c 5-11 ) 
		site4=$(grep -w "${site4_full}" ${all_atoms_list} | cut -c 5-11 )  
		site5=$(grep -w "${site5_full}" ${all_atoms_list} | cut -c 5-11 ) 
		site6=$(grep -w "${site6_full}" ${all_atoms_list} | cut -c 5-11 )  
		sed -i "/${site1}/d" ${atom_list_remove}
		sed -i "/${site2}/d" ${atom_list_remove}
		sed -i "/${site3}/d" ${atom_list_remove}
		sed -i "/${site4}/d" ${atom_list_remove}
		sed -i "/${site5}/d" ${atom_list_remove}
		sed -i "/${site6}/d" ${atom_list_remove}

	elif [[ "${number_of_sites}" -eq "8" ]]; then 
		# Identifying the eight sites
		site1_full=$(echo ${BASE_2UP} | cut -c 4-6)
		site2_full=$(echo ${BASE_2UP} | cut -c 8-10)
		site3_full=$(echo ${BASE_2UP} | cut -c 12-14)
		site4_full=$(echo ${BASE_2UP} | cut -c 16-18)
		site5_full=$(echo ${BASE_2UP} | cut -c 20-22)
		site6_full=$(echo ${BASE_2UP} | cut -c 24-26)
		site7_full=$(echo ${BASE_2UP} | cut -c 28-30)
		site8_full=$(echo ${BASE_2UP} | cut -c 32-34)
		site_file_info=$(echo ${BASE_2UP} | cut -c 4-26)
		
		# Collecting and deleting the site information 
		site1=$(grep -w "${site1_full}" ${all_atoms_list} | cut -c 5-11 ) 
		site2=$(grep -w "${site2_full}" ${all_atoms_list} | cut -c 5-11 ) 
 		site3=$(grep -w "${site3_full}" ${all_atoms_list} | cut -c 5-11 ) 
		site4=$(grep -w "${site4_full}" ${all_atoms_list} | cut -c 5-11 )  
		site5=$(grep -w "${site5_full}" ${all_atoms_list} | cut -c 5-11 ) 
		site6=$(grep -w "${site6_full}" ${all_atoms_list} | cut -c 5-11 )  
		site7=$(grep -w "${site7_full}" ${all_atoms_list} | cut -c 5-11 ) 
		site8=$(grep -w "${site8_full}" ${all_atoms_list} | cut -c 5-11 )  
		sed -i "/${site1}/d" ${atom_list_remove}
		sed -i "/${site2}/d" ${atom_list_remove}
		sed -i "/${site3}/d" ${atom_list_remove}
		sed -i "/${site4}/d" ${atom_list_remove}
		sed -i "/${site5}/d" ${atom_list_remove}
		sed -i "/${site6}/d" ${atom_list_remove}
		sed -i "/${site7}/d" ${atom_list_remove}
		sed -i "/${site8}/d" ${atom_list_remove}

	elif [[ "${number_of_sites}" -eq "10" ]]; then 
		# Identifying the eight sites
		site1_full=$(echo ${BASE_2UP} | cut -c 4-6)
		site2_full=$(echo ${BASE_2UP} | cut -c 8-10)
		site3_full=$(echo ${BASE_2UP} | cut -c 12-14)
		site4_full=$(echo ${BASE_2UP} | cut -c 16-18)
		site5_full=$(echo ${BASE_2UP} | cut -c 20-22)
		site6_full=$(echo ${BASE_2UP} | cut -c 24-26)
		site7_full=$(echo ${BASE_2UP} | cut -c 28-30)
		site8_full=$(echo ${BASE_2UP} | cut -c 32-34)
		site9_full=$(echo ${BASE_2UP} | cut -c 36-38)
		site10_full=$(echo ${BASE_2UP} | cut -c 40-42)
		site_file_info=$(echo ${BASE_2UP} | cut -c 4-42)
		
		# Collecting and deleting the site information 
		site1=$(grep -w "${site1_full}" ${all_atoms_list} | cut -c 5-11 ) 
		site2=$(grep -w "${site2_full}" ${all_atoms_list} | cut -c 5-11 ) 
 		site3=$(grep -w "${site3_full}" ${all_atoms_list} | cut -c 5-11 ) 
		site4=$(grep -w "${site4_full}" ${all_atoms_list} | cut -c 5-11 )  
		site5=$(grep -w "${site5_full}" ${all_atoms_list} | cut -c 5-11 ) 
		site6=$(grep -w "${site6_full}" ${all_atoms_list} | cut -c 5-11 )  
		site7=$(grep -w "${site7_full}" ${all_atoms_list} | cut -c 5-11 ) 
		site8=$(grep -w "${site8_full}" ${all_atoms_list} | cut -c 5-11 )  
		site9=$(grep -w "${site9_full}" ${all_atoms_list} | cut -c 5-11 ) 
		site10=$(grep -w "${site10_full}" ${all_atoms_list} | cut -c 5-11 )  
	
		sed -i "/${site1}/d" ${atom_list_remove}
		sed -i "/${site2}/d" ${atom_list_remove}
		sed -i "/${site3}/d" ${atom_list_remove}
		sed -i "/${site4}/d" ${atom_list_remove}
		sed -i "/${site5}/d" ${atom_list_remove}
		sed -i "/${site6}/d" ${atom_list_remove}
		sed -i "/${site7}/d" ${atom_list_remove}
		sed -i "/${site8}/d" ${atom_list_remove}
		sed -i "/${site9}/d" ${atom_list_remove}
		sed -i "/${site10}/d" ${atom_list_remove}

	fi	
	
	echo ' - - - - - - - - - - - - - - - '
	echo '' 
	echo "${site_file_info}" 
	echo '' 
	echo ' - - - - - - - - - - - - - - - '

	# Looking up directory information
	DIR=$(pwd)
	DIR_1UP="$(dirname "${DIR}")"
	BASE_1UP="$(basename "${DIR_1UP}")"
	DIR_2UP="$(dirname "${DIR_1UP}")"
	BASE_2UP="$(basename "${DIR_2UP}")"
	
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

	sed -i "s/ENTERJOBNAME/${site_file_info}/g" ${input_file}-modified
	sed -i "s/${number_of_atoms}/       NUMBER_OF_ATOMS ${new_atoms_count}/g" ${input_file}-modified
	sed -i "s/${number_of_atoms_number}/${number_atoms_remove}/g" ${input_file%.*}-atoms-removed.xyz
	sed -i "s/${number_of_atoms_number}/${new_atoms_count}/g" ${input_file%.*}.xyz  

	cp ${input_file} ${input_file}-origin
	cp ${input_file}-modified ${input_file} 

	new_filename="${input_file%.*}${site_file_info}"
	
	mv ${input_file%.*}-atoms-removed.xyz ${new_filename}-atoms-removed.xyz
	mv ${input_file%.*}.xyz ${new_filename}.xyz
	
	mkdir 00-OUTPUT 01-VIS

	mv *xyz 01-VIS/. 
	mv *inp* 00-OUTPUT/.
	mv 00-OUTPUT/${input_file} .
	
	new_filename="${input_file%.*}${site_file_info}"
	
	cp ${input_file} ${DIR_1UP}/${new_filename}.inp

	sed -i "s/ENTERJOBNAME/${site_file_info}/g" ${DIR_1UP}/sub*.sh

else
	echo ' - - - - - - - - - - - - - - - '
	echo '' 
	echo 'You are missing a file!'
	echo ''
	echo ' - - - - - - - - - - - - - - - '
fi


 
