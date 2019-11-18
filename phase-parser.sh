#!/usr/bin/env bash
#
# Stephen Patrick Vicchio
# 2019-11-11 
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 
# This script now finds all of the zp files and reads their information along with the 
# reported energy from CP2K.   
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  

# Specifying the workdir for the jobs 
WORKDIR=${PWD}


# Printing the Headers for any potential file
	printf '%-12s' "  P H A S E "
	printf '%-3s'  " | "
	printf '%-38s' "            E N E R G Y (a.u.)        "	
	printf '%-3s'  " | "
	printf "               D I R E C T O R Y            "
	echo -e '\n'	
	printf '%-12s' " ---------- "
	printf '%-3s'  " | "
	printf '%-38s' " ------------------------------------ "	
	printf '%-3s'  " | "
	printf " ------------------------------------------ "
	echo -e '\n'	
	

# Generating the list of files to parse
list_of_zp_files=$(find . -name zp*) 

# Parsing all of the zp-files and directories for energies
for i in ${list_of_zp_files}; do
	# Finding the phase information 
	phase_info=$(grep "phase" ${i} | awk '{print $3}')
	
	# Determining the phase directory	
	PHASEDIR=$(dirname ${i})

	if [[ ${PHASEDIR} == *"00-OUTPUT"* ]]; then
		# Determining the OUTPUT energy 
		energy_info=$(grep "ENERGY|" ${PHASEDIR}/*out | awk '{print $9}' | tail -1)
	
	        # writing to a file
#		echo -e '- - - \n'
		printf '%-12s' " Phase: ${phase_info} "
		printf '%-3s'  " | "
		printf '%-38s' " Energy (a.u.): ${energy_info} "	
		printf '%-3s'  " | "
		printf " Dir: ${PHASEDIR}"
		echo -e '\n'	
	fi 	
done






