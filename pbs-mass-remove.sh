#!/usr/bin/env bash
#
# Stephen Patrick Vicchio
# 2019-07-05 
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 
# simple script to delete a job 
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  

JOBID_NUM_START=${1%.*}
JOBID_NUM_FINISH=${2%.*}

for i in $(seq ${JOBID_NUM_START} 1 ${JOBID_NUM_FINISH}); do
	qdel ${i}
done 

