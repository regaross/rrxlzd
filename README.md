# rrxlzd

Personal toolkit for **XLZD** simulation work: scripts to run Geant4 jobs on SLAC S3DF, inspect detector geometry locally, and (over time) analyze simulation output.

This repo is not the XLZD Geant4 application itself. The simulation lives in [`xlzd-sandbox`](https://gitlab.com/XLZD-UK/xlzd-sandbox); collaboration helpers for S3DF are in [`Sandbox-SLAC`](https://gitlab.com/XLZD-Collaboration/simulation/Sandbox-SLAC). Here you will find wrappers, macros workflow, and notes.

## What’s in here

| Path | Role |
|------|------|
| [`submit.sh`](submit.sh) | SLURM batch submission (outside the container) |
| [`run_biased.sh`](run_biased.sh) | In-container runner for biased `xlzd` jobs |
| [`scripts/viz_gdml.py`](scripts/viz_gdml.py) | Local Mac GDML geometry viewer (pyg4ometry + VTK) |
| [`docs/`](docs/) | Setup, running, and visualization notes |

## Dependencies

Work splits across two environments. You typically do **not** need everything on one machine.

### S3DF (simulation execution)

Required to build and run `xlzd` jobs:

| Dependency | Where / notes |
|------------|----------------|
| SLAC S3DF account + XLZD group access | `/sdf/group/fpd/xlzd/` |
| [Apptainer](https://apptainer.org/) | Container runtime on S3DF |
| `xlzd_sandbox_rocky9.sif` | `/sdf/group/fpd/xlzd/software/xlzd_sandbox_rocky9.sif` |
| CVMFS Geant4 stack | Mounted from `/cvmfs/` inside the container |
| [`xlzd-sandbox`](https://gitlab.com/XLZD-UK/xlzd-sandbox) | Clone under your user space; build with `source setup.sh && make` |
| SLURM | Job submission (`sbatch`, `squeue`, …) |
| [`Sandbox-SLAC`](https://gitlab.com/XLZD-Collaboration/simulation/Sandbox-SLAC) | Optional upstream submit helpers; this repo’s `submit.sh` / `run_biased.sh` are a biased-run variant |

Official references:

- [XLZD sandbox docs](https://xlzd-collaboration.gitlab.io/simulation/xlzd-sandbox/quickstart.html)
- [Sandbox-SLAC](https://gitlab.com/XLZD-Collaboration/simulation/Sandbox-SLAC)

### Local Mac (geometry visualization / analysis)

Required for [`scripts/viz_gdml.py`](scripts/viz_gdml.py) and future ROOT-based analysis:

| Dependency | Notes |
|------------|--------|
| Conda env `xlzd` | Working environment for local tools |
| [ROOT](https://root.cern/) | In `xlzd` (analysis; **not** for XLZD GDML import — see below) |
| [pyg4ometry](https://pyg4ometry.readthedocs.io/) + [VTK](https://vtk.org/) | GDML load + interactive 3D view |
| Homebrew [OpenCASCADE](https://www.opencascade.com/) | `brew install opencascade` — needed for pyg4ometry’s CAD bindings to import cleanly |

XLZD GDMLs use Geant4 `multiUnion` solids. ROOT’s `TGeo` GDML importer does not support those tags, so geometry viewing goes through pyg4ometry/VTK, not ROOT.

Quick check:

```bash
brew install opencascade   # once
conda activate xlzd
python -c "import ROOT, pyg4ometry, vtk; print('ok')"
```

## Quick starts

### Run a biased simulation on S3DF

After the sandbox is built inside the Apptainer (see [docs/setup.md](docs/setup.md)):

```bash
sbatch --array=0-20 -o out/slurm_%A_%a.out submit.sh path/to/macro.mac
```

Details and bind-path notes: [docs/running.md](docs/running.md).

### View a GDML on your Mac

```bash
conda activate xlzd
python scripts/viz_gdml.py /path/to/geometry.gdml --list
python scripts/viz_gdml.py /path/to/geometry.gdml --volume TPC_L
```

Prefer a focused `--volume` (e.g. `TPC`, `Skin`, `OCV`) over the full world volume. Full notes: [docs/visualizing.md](docs/visualizing.md).

## Documentation

- [Purpose & links](docs/intro.md)
- [S3DF setup](docs/setup.md)
- [Running jobs](docs/running.md)
- [Local geometry visualization](docs/visualizing.md)

## Scope

This repository will grow with analysis scripts and execution helpers as the XLZD workflow matures. Large geometry files (GDML) and simulation ROOT outputs are kept outside the repo.
