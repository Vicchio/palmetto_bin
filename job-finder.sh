#!/usr/bin/env bash
#
# Stephen Patrick Vicchio
# 2019-11-14444 
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 
# Identifies the phase of an older job!  
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  

job_find_dir=${1}

if [[ -z ${job_find_dir} ]]; then 
	echo ''
	echo 'Please specify a ####### to find.'
	echo ''
else
	cd /curium/svicchi/
	JOBID=${job_find_dir}
	JOBID_ZC_FILE=$(find . -name *${JOBID}*)
	JOBID_DIR=$(dirname ${JOBID_ZC_FILE})
	cd ${JOBID_DIR}
fi 
