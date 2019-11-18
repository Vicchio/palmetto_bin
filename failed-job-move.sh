#!/usr/bin/env bash
#
# Stephen Patrick Vicchio
# 2019-07-05 
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 
# moves files over from unfinished job 
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  


if [[ -z ${1} ]]; then 
	echo ''
	echo 'Please specify a zc-#######.JOBID to copy'
	echo ''
else


# Setting up the search parameters
JOBID_NAME=${1%.*}
JOBID_MOVE=$(echo ${JOBID_NAME} | cut -c 4- )
SCRATCH_DIR=/scratch1/svicchi/VASP-${JOBID_MOVE}.pbs02

# Copying files back to submit directory 
declare -a COPY_LIST=("INCAR" "KPOINTS" "POSCAR" "POTCAR" "REPORT" "IBZKPT" "PCDAT" "XDATCAR" "CONTCAR" \
			"OSZICAR" "EIGENVAL" "vasprun.xml" "OUTCAR" "DOSCAR")
mkdir -p ${PWD}/00-OUTPUT

for i in "${COPY_LIST[@]}"; do
	cp ${SCRATCH_DIR}/${i} ${PWD}/00-OUTPUT/.
done 

# Creating the visualization directory 
mkdir -p ${PWD}/01-VIS 
declare -a COPY_LIST=("POSCAR" "XDATCAR" "CONTCAR")
for i in "${COPY_LIST[@]}"; do
	cp ${PWD}/00-OUTPUT/${i} ${PWD}/01-VIS/. 
done 

# Creating job restart directory
mkdir -p ${PWD}/02-RESTART 
declare -a COPY_LIST=("CONTCAR" "INCAR" "POTCAR" "KPOINTS")
for i in "${COPY_LIST[@]}"; do
	cp ${PWD}/00-OUTPUT/${i} ${PWD}/02-RESTART/. 
done 
mv ${PWD}/02-RESTART/CONTCAR ${PWD}/02-RESTART/CONTCAR-${JOBID_MOVE}.pbs02
cp ${PWD}/02-RESTART/CONTCAR-${JOBID_MOVE}.pbs02 ${PWD}/02-RESTART/POSCAR
 

fi 
