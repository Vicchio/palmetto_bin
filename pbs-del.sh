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

JOBID_NAME=${1%.*}
JOBID_DEL=$(echo ${JOBID_NAME} | cut -c 4- )
qdel ${JOBID_DEL}

