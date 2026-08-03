# Visualizing detector geometry locally (Mac)

Use this when you want to look at an XLZD Geant4 geometry on your laptop without running the full simulation stack.

## Why not ROOT?

ROOT is available in the `xlzd` conda env, but its GDML importer (`TGeoManager::Import`) does **not** support Geant4 `multiUnion` solids. XLZD exports (e.g. `simple_boosting.gdml`) use those solids, so ROOT aborts on import.

Prefer **pyg4ometry + VTK** instead.

## Prerequisites

1. Conda env `xlzd` with `pyg4ometry` and `vtk` (already present if you followed the usual setup).
2. Homebrew OpenCASCADE so pyg4ometry’s CAD bindings can load (even if you only view GDML):

```bash
brew install opencascade
conda activate xlzd
python -c "import pyg4ometry; print('ok')"
```

If OpenCASCADE is missing, `scripts/viz_gdml.py` tries a soft fallback that stubs the CAD modules and continues with GDML + VTK only.

## Usage

From the `rrxlzd` repo root:

```bash
conda activate xlzd

# List logical volumes
python scripts/viz_gdml.py ../gdml/simple_boosting.gdml --list

# Interactive VTK viewer (world volume — often huge / slow)
python scripts/viz_gdml.py ../gdml/simple_boosting.gdml

# Focus on a detector region (recommended)
python scripts/viz_gdml.py ../gdml/simple_boosting.gdml --volume TPC
python scripts/viz_gdml.py ../gdml/simple_boosting.gdml --volume Skin
python scripts/viz_gdml.py ../gdml/simple_boosting.gdml --volume OCV
```

`--volume` matches the first logical volume whose name contains the substring (case-insensitive). Prefer a more specific substring if several volumes match.

Listing volumes is fast (meshing is deferred). The first draw of a region that
contains large `multiUnion` solids can take a while; that is expected. Prefer
`--volume TPC` (or similar) over the full world volume.

## Getting a GDML from the S3DF sandbox

On S3DF, inside the XLZD sandbox / Geant4 app, export geometry with whatever GDML write path the sandbox supports (or a `/geometry/...` macro if available), then copy the `.gdml` file to your Mac (e.g. under `../gdml/` next to this repo) and point `viz_gdml.py` at it.

Large GDML files are intentionally kept outside `rrxlzd` rather than committed.
