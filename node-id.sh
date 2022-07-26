#!/usr/bin/env bash
#
# Stephen Patrick Vicchio
# 2019-07-05 
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 
# simple script to determine what phase the job is currently running on  
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  


PBS_FILE=$(ls *.sh)
PBS_JOB=$(grep "PBS -N" ${PBS_FILE} | awk '{ print $3 }')


# Determining Job information 
JOBID_NAME=${1%.*}
JOBID=$(echo ${JOBID_NAME} | cut -c 4- )
FILE_READ=$(ls *.o${JOBID})
node_ID=$(grep "exec_host" ${FILE_READ} | awk '{ print $3 }' | cut -c -8)
phase_info=$(pbsnodes ${node_ID} | grep resources_available.phase | awk '{print $3}')



# Printing out information 
echo "-----------------------------"
echo "     JOB: ${PBS_JOB}"
echo "    Node: ${node_ID}"
echo "   Phase: ${phase_info}"
echo "-----------------------------"

