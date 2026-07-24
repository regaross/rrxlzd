# Setup

We'll loosely follow the setup instructions as found in [Brian Mong's instructions](https://gitlab.com/XLZD-Collaboration/simulation/Sandbox-SLAC#sandbox-slac), in the [documentation](https://xlzd-collaboration.gitlab.io/simulation/xlzd-sandbox/index.html), and in the [simulation workshop slides](https://drive.google.com/drive/folders/1bUalItejtW5gK9PjM4p-a4W_Lb1InQcd). The plan is to document the process as it happens and ensure that errors are addressed, and files that need adjusting get adjusted appropriately.

## Installation

### 1. Get the Code


The simulation repo is [here](https://gitlab.com/XLZD-Collaboration/simulation/xlzd-sandbox). We need to clone the repo:

```bash
# Change to your directory in the XLZD space
cd /sdf/group/fpd/xlzd/users/$USER
```
Contact Brian Mong if you can't do this.
```bash
# Clone the repo
git clone git@gitlab.com:XLZD-UK/xlzd-sandbox.git
```

### 2. Source and Boot Container

The fundamental building blocks to the simulation, namely the independent G4 source code and its dependencies are already on S3DF. Cern has what's called the [CVMFS](https://cvmfs.readthedocs.io/en/stable/) through which they distribute the software, including G4 dependencies. On S3Df, we have this. Necessary dependencies exist on S3DF inside `/cvmfs/`. 

Other dependencies for the XLZD simulation— environment variables and the like— are set up inside an "apptainer". You can imagine this as a house in which you will be doing work. There are doors out of the house to access files in the neighbourhood (your directories). This container is saved on the server and accessible here:

```bash
/sdf/group/fpd/xlzd/software/xlzd_sandbox_rocky9.sif
```

Now make a quick script for booting the apptainer, call it `bootapptainer.sh`:
```bash
#!/bin/bash

apptainer shell --home /sdf/group/fpd/xlzd/users/$USER/ \
--pwd /sdf/group/fpd/xlzd/users/$USER/ \
--bind /cvmfs,/sdf/group/fpd/xlzd/,/sdf/data/fpd/xlzd/,\
/sdf/group/fpd/xlzd/users/$USER/xlzd-sandbox:\
/opt/xlzd-sandbox /sdf/group/fpd/xlzd/software/xlzd_sandbox_rocky9.sif
```

The `-bind` bind-mounts a few directories so that they're accessible from within the container. `/cvmfs/` is the Cern software directory. This is kind of like requesting that your house be hooked up to utilities. Now, you can access the CERN software inside the container. The command will boot a new interactive `shell`— you're now doing stuff from within the container. Your working directory will be your personal directory in `..../xlzd/users/`. You also have access to the data storage directory `/sdf/data/fpd/xlzd/`. 

Then run the following to make sure you have permission to run it:

```bash
chmod +x bootapptainer.sh
```
Then boot it!

```bash
./bootapptainer.sh
```

### 3. Build the Simulation
The code then needs to be compiled so that you have an `xlzd` executable that can run the desired simulations. **Make sure you have booted the container as in step 2!**

Set up the environment variables:

```bash
cd /opt/xlzd-sandbox
source setup.sh
```
Then we compile the simulation code:

```bash
make -j2
```

#### What now?

There should be an executable file `xlzd`. It lives in `./xlzd-sandbox/build` but is now an environment variable.

### A quick example
Assuming you've booted the container with your saavy `bootapptainer.sh` script, here's how you can run a quick example to see that everything is functional:

```bash
cd /opt/xlzd-sandbox
xlzd --mac templates/macros/particle.mac
```

You should have produced an output file, `Output.root` in `xlzd-sandbox`. And no *obvious* errors should have occurred.