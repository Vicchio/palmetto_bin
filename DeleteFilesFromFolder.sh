#!/bin/bash
##############    Start Edit   ##############
#Check folder size
#du -c ./foldername/
cwd=$(pwd)
echo "Initial Folder Size"
du -s -h ${cwd}
#Files to delete
filesname=(.wfn .wfn.bak-1 .wfn.bak-2 .wfn.bak-3)
##############    End Edit   ##############

#arr=($filesname)          #Convert to a list
Llen=${#filesname[@]} 
for i in $(seq 1 1 $Llen)
do
j=$(($i -1))
echo "------------------------------------------------------------------"
echo $i
echo ${filesname[j]} 
echo "------------------------------------------------------------------"
	for file in $(find . -iname *${filesname[j]}) 
	do 
#	echo $file
	rm -rf $file
	done
done

cwd=$(pwd)
echo "Final Folder Size"
du -s -h ${cwd}
