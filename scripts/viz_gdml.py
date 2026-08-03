#!/usr/bin/env python3
"""Interactive GDML geometry viewer using pyg4ometry + VTK.

XLZD GDMLs use Geant4 multiUnion solids that ROOT's TGeo importer does not
support. Prefer this script (conda env: xlzd) for local Mac visualization.

Usage:
  conda activate xlzd
  python scripts/viz_gdml.py ../gdml/simple_boosting.gdml --list
  python scripts/viz_gdml.py ../gdml/simple_boosting.gdml --volume TPC
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _stub_opencascade_cad_modules() -> None:
    """Pre-seed empty CAD modules so pyg4ometry can import without OpenCASCADE.

    pyg4ometry's convert package eagerly imports oce2Geant4/vis2oce, which load
    native OpenCASCADE bindings. Those are unused for GDML + VTK viewing.
    """
    import types

    for name in (
        "pyg4ometry.pyoce",
        "pyg4ometry.convert.oce2Geant4",
        "pyg4ometry.convert.vis2oce",
    ):
        if name not in sys.modules:
            mod = types.ModuleType(name)
            mod.__all__ = []  # type: ignore[attr-defined]
            sys.modules[name] = mod


def _import_pyg4ometry():
    try:
        import pyg4ometry

        return pyg4ometry
    except Exception as first:
        try:
            doomed = [
                k for k in list(sys.modules) if k == "pyg4ometry" or k.startswith("pyg4ometry.")
            ]
            for k in doomed:
                del sys.modules[k]
            _stub_opencascade_cad_modules()
            import pyg4ometry

            print(
                "Warning: pyg4ometry CAD/OpenCASCADE bindings unavailable; "
                "continuing with GDML + VTK only.",
                file=sys.stderr,
            )
            return pyg4ometry
        except Exception as second:
            print(
                "Failed to import pyg4ometry.\n"
                "The xlzd conda env needs pyg4ometry + VTK. If CAD bindings are "
                "broken, install Homebrew OpenCASCADE:\n"
                "  brew install opencascade\n"
                "  conda activate xlzd\n"
                "  python -c 'import pyg4ometry'\n"
                f"\nOriginal error: {first}\n"
                f"Fallback error: {second}",
                file=sys.stderr,
            )
            raise SystemExit(1) from second


def _logical_volumes(registry):
    return sorted(registry.logicalVolumeDict.keys())


def _resolve_volume(registry, volume_substr: str | None):
    if not volume_substr:
        return registry.getWorldVolume(), registry.getWorldVolume().name

    matches = [n for n in _logical_volumes(registry) if volume_substr.lower() in n.lower()]
    if not matches:
        print(f"No logical volume matching {volume_substr!r}.", file=sys.stderr)
        print("Use --list to see available names.", file=sys.stderr)
        raise SystemExit(2)

    # Prefer exact (case-insensitive) match, else shortest name (usually the
    # primary LV rather than a long pointer-suffixed duplicate).
    exact = [n for n in matches if n.lower() == volume_substr.lower()]
    chosen = exact[0] if exact else sorted(matches, key=len)[0]
    if len(matches) > 1 and not exact:
        print(
            f"Multiple matches for {volume_substr!r}; using {chosen!r} "
            f"({len(matches)} matches). Pass a more specific --volume.",
            file=sys.stderr,
        )
    return registry.logicalVolumeDict[chosen], chosen


def _collect_unique_logicals(logical, seen: set[int] | None = None) -> list:
    """Return unique logical volumes under ``logical`` in visit order."""
    if seen is None:
        seen = set()
    out = []
    key = id(logical)
    if key in seen:
        return out
    seen.add(key)

    if getattr(logical, "type", None) == "logical":
        out.append(logical)

    for daughter in getattr(logical, "daughterVolumes", []) or []:
        child = getattr(daughter, "logicalVolume", None)
        if child is not None:
            out.extend(_collect_unique_logicals(child, seen))
    return out


def _remesh_unique(logical) -> None:
    """Mesh each logical volume once, printing progress to stderr."""
    volumes = _collect_unique_logicals(logical)
    total = len(volumes)
    print(f"Meshing {total} unique logical volume(s) ...", file=sys.stderr, flush=True)
    for i, vol in enumerate(volumes, start=1):
        name = getattr(vol, "name", "?")
        solid_type = getattr(getattr(vol, "solid", None), "type", "?")
        print(
            f"  [{i}/{total}] {name} ({solid_type})",
            file=sys.stderr,
            flush=True,
        )
        vol.reMesh(recursive=False)
    print("Meshing done.", file=sys.stderr, flush=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Visualize a Geant4 GDML geometry with pyg4ometry + VTK."
    )
    parser.add_argument("gdml", type=Path, help="Path to a .gdml file")
    parser.add_argument(
        "--list",
        action="store_true",
        help="List logical volume names and exit",
    )
    parser.add_argument(
        "--volume",
        metavar="SUBSTR",
        help="Draw the first logical volume whose name contains SUBSTR "
        "(case-insensitive). Default: world volume.",
    )
    parser.add_argument(
        "--wireframe-world",
        action="store_true",
        help="Also draw the selected volume bounding solid as wireframe",
    )
    args = parser.parse_args(argv)

    gdml_path = args.gdml.expanduser().resolve()
    if not gdml_path.is_file():
        print(f"GDML file not found: {gdml_path}", file=sys.stderr)
        return 1

    pyg4ometry = _import_pyg4ometry()

    # XLZD GDMLs contain large multiUnions; meshing every LV on load is
    # prohibitively slow. Parse structure first, mesh only what we draw.
    pyg4ometry.config.doMeshing = False

    print(f"Loading {gdml_path} ...", file=sys.stderr, flush=True)
    reader = pyg4ometry.gdml.Reader(str(gdml_path))
    registry = reader.getRegistry()
    print("GDML parse complete.", file=sys.stderr, flush=True)

    names = _logical_volumes(registry)
    if args.list:
        for name in names:
            print(name)
        print(f"\n{len(names)} logical volumes", file=sys.stderr, flush=True)
        return 0

    lv, lv_name = _resolve_volume(registry, args.volume)
    print(f"Drawing logical volume: {lv_name}", file=sys.stderr, flush=True)
    print(
        "Note: large multiUnion solids can take a long time per volume.",
        file=sys.stderr,
        flush=True,
    )
    _remesh_unique(lv)

    print("Building VTK scene ...", file=sys.stderr, flush=True)
    viewer = pyg4ometry.visualisation.VtkViewerColouredMaterial()
    # pyg4ometry's addLogicalVolume only surfaces *daughter* placements; the
    # root solid itself is optional wireframe via addWorld. Leaf volumes
    # (e.g. TPC) therefore need an explicit solid draw.
    n_daughters = len(getattr(lv, "daughterVolumes", []) or [])
    if n_daughters == 0:
        viewer.addSolid(lv.solid, representation="surface", opacity=0.6)
    else:
        viewer.addLogicalVolume(
            lv,
            recursive=True,
            addWorld=args.wireframe_world,
        )
    print("Opening viewer ...", file=sys.stderr, flush=True)
    viewer.view()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
