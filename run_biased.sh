#!/bin/bash

source /opt/xlzd-sandbox/setup.sh

# The main argument is the mac file, no path attached here.
export MAC_FILE="$1"
export MACFILENAME=$(basename "${MAC_FILE%.*}")
export MACFOLDNAME=$(dirname "$MAC_FILE")
export ROOTFILE="/lscratch/${MACFILENAME}_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.root"

mkdir -p ${MACFOLDNAME}/root_files
mkdir -p ${MACFOLDNAME}/macros
export NEW_MAC_FILE="${MACFOLDNAME}/macros/${MACFILENAME}_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.mac"

envsubst < ${MAC_FILE} >> ${NEW_MAC_FILE}
# cp ${MAC_FILE} ${NEW_MAC_FILE}

# We need to change the output file, and the seeds, make sure we collect the root file, and then we're good!



xlzd --mac ${NEW_MAC_FILE} --biasing 1

mv ${ROOTFILE} ${MACFOLDNAME}/root_files/

# # # The file that's like eventBiasing.mac
# # export MAC_FILE_B="$2"


# # mkdir -p ${MACFOLDNAME}/out

# # Copies the environment variables into the "$1" which is the macro and saves it to the new location.

# echo "this is before the execution"
# echo $PWD
# echo "${MACFOLDNAME}/macros/${MACFILENAME}_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.mac"

# # Starting XLZD SIM 
# xlzd --mac ${MACFOLDNAME}/macros/${MACFILENAME}_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.mac --biasing 0

# echo "this is after the execution"

# # #Output handling
# # mkdir -p /sdf/group/fpd/xlzd/users/$USER/${MACFOLDNAME}/macros

# # mv /lscratch/${MACFILENAME}_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.root ${MACFOLDNAME}/root_files/