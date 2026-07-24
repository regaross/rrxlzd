# Running Simulations

In general, on S3DF, jobs are run via submissions to the job manager, `SLURM`. Brian Mong put together a convenient mini-repo of scripts that make this an easier process.

### 1. Clone the S3DF-specific tool repo

```bash
cd /sdf/group/fpd/xlzd/users/$USER
git clone https://gitlab.com/XLZD-Collaboration/simulation/Sandbox-SLAC.git
```

### 2. Adjust the shell scripts
There are two critical shell scripts in Sandbox-SLAC. They are `run_sim.sh` and `submit.sh`.  `run_sim.sh` is run from within the container. `submit.sh` is run from outside the container.

The final command in `submit.sh` will need to be adjusted for you:

From:
```bash
apptainer exec  \
          --bind /lscratch,/cvmfs,/sdf/group/fpd/xlzd/,/sdf/data/fpd/xlzd/,/sdf/group/fpd/xlzd/users/bmong/xlzd-sandbox:/opt/xlzd-sandbox \
          $APPIMG /bin/bash run_sim.sh ${1}
```

to:

```bash
apptainer exec  \
          --bind /lscratch,/cvmfs,/sdf/group/fpd/xlzd/,/sdf/data/fpd/xlzd/,/sdf/group/fpd/xlzd/users/$USER/xlzd-sandbox:/opt/xlzd-sandbox \
          $APPIMG /bin/bash run_sim.sh ${1}

```

You shouldn't need to change `run_sim.sh` in any meaningful way, but you may want to adjust lines 57 through 60 to ensure files are stored in the proper locations. The following substitution makes sure the root file output gets saved to your project folder.

```bash
#Copy output files of the simulation, root and macro
mkdir -p /sdf/group/fpd/xlzd/users/$USER/${MACFOLDNAME}/macros
# mkdir -p /sdf/group/fpd/xlzd/users/$USER/${MACFOLDNAME}/root_files
mv /lscratch/${MACFILENAME}_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.root ${MACFOLDNAME}/root_files/
#mv ${MACFOLDNAME}/macros/${MACFILENAME}_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.mac /sdf/group/fpd/xlzd/users/$USER/${MACFOLDNAME}/macros/
```

### 3. Run something

Make a folder, probably in `/xlzd/users/$USER/` for the simulation you're trying to run.




# Event Biasing

### EB.mac

### eventBiasing.mac
