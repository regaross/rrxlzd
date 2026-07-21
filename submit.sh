#!/bin/bash
#SBATCH --job-name=xlzdsim
#SBATCH --partition=milano
#SBATCH --account=exo:default
#SBATCH --output=out/slurm-%A_%a.out
#SBATCH --qos=preemptable
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --mem-per-cpu=3G
#SBATCH --time=03:00:00
#
# milano machines have 12O cores and 480GB memory (4GB/core)
# Time guidence: 16k events in 20min, 50k in ~1hr
# To Run: 
#    sbatch --array=0-20 -o out/slurm_%A_%a.out submit.sh gamma2600_ICV.mac
# Will execute 21 single tasks with unique seeds based on task_ID 
# You can monitor your runs via:
#    squeue --user=<username>
# You can cancel a job 
#        scancel <JOB_ID>
# Or all of your jobs via
#        scancel --me 
# -or-   scancel --user=<username>


# This container is made simply by converting the docker image to sif:
#    apptainer pull xlzd_sandbox_rocky9.sif docker://xlzdg3/xlzd_sandbox:rocky9
APPIMG=/sdf/group/fpd/xlzd/software/xlzd_sandbox_rocky9.sif

echo "Starting a job ${1} ${SLURM_ARRAY_TASK_ID} / ${SLURM_ARRAY_JOB_ID}"

apptainer exec  \
          --bind /lscratch,/cvmfs,/sdf/group/fpd/xlzd/,/sdf/data/fpd/xlzd/,/sdf/group/fpd/xlzd/users/rross/xlzd-sandbox:/opt/xlzd-sandbox \
          $APPIMG /bin/bash run_biased.sh ${1}

