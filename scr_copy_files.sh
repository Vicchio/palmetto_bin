#!/usr/bin/env bash
#
# Stephen Patrick Vicchio
# 2021-12-27 
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 
# script to copy over all files from the cluster to my local directory
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  

# the directories for my calculations
work_dir=$PWD
scr_dir=$(cat zb-TO-*)

# dir for the OPT files
if [ -d "${scr_dir}/00-opt/" ]; then
	cp ${scr_dir}/00-opt/* ${work_dir}/00-opt/.
fi


# dir for the STABLE files
if [ -d "${scr_dir}/01-stable/" ]; then
	cp ${scr_dir}/01-stable/* ${work_dir}/01-stable/.
fi


# dir for the FREQ files
if [ -d "${scr_dir}/02-freq/" ]; then
	cp ${scr_dir}/02-freq/* ${work_dir}/02-freq/.
fi


