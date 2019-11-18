#!/usr/bin/env bash
#
# Stephen Patrick Vicchio
# 2019-11-11 
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 
# Identifies the phase of an older job!  
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  

WORKDIR=$PWD
input_file=${1}

if [[ -z ${input_file} ]]; then 
	echo ''
	echo 'Please specify a zc-#######.JOBID to copy'
	echo ''
elif [[ ${input_file} != *.JOBID ]]; then 
	echo ''
	echo 'Please specify a zc-#######.JOBID to copy'
	echo ''
else
	JOBID_NAME=${input_file%.*}
	JOBID_MOVE=$(echo ${JOBID_NAME} | cut -c 4- )
	node_info_cut=$(grep -m 1 "exec_host" *o${JOBID_MOVE} | awk '{print $3}' | cut -c1-8)
	line_number_resources_availible=$(pbsnodes ${node_info_cut} | grep resources_available.phase)
	echo -e 'Node: ' ${node_info_cut} > ${WORKDIR}/zp-phase.PHASE
	echo -e 'The calculation is currently running on: \n' ${line_number_resources_availible} >> ${WORKDIR}/zp-phase.PHASE
fi 
