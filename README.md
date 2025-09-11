# OpenMRD — Open MRI Design Format

OpenMRD is a **human‑readable, interoperable** file and folder standard for **open-source MRI scanner design and fabrication**, with a focus on **low-field systems**. Think of it as doing for **hardware design** what **Pulseq** did for **sequence design**.

## Goals
- Portable designs across labs and vendors.
- Reproducible fabrication and assembly.
- Clear coordinate systems & units.
- Extensible to different magnet and coil geometries (Halbach, C-, H-type, cylindrical, planar).
- Validation & versioning baked in.

## Core concepts
- A repository (or zip) is an **OpenMRD package**.
- The package has a top-level manifest: `scanner.yaml`.
- All CAD/fieldmaps/BOM/test data live in subfolders and are referenced by relative paths with checksums.
- JSON Schema + Pydantic validate the manifest.
- Everything uses **SI units**, **right-handed RAS** scanner coordinates by default (configurable via transforms).

## Quick start (CLI)
```bash
python3 -m venv openmrd
source openmrd/bin/activate
pip install -e .
openmrd init my_scanner --template halbach_lowfield
openmrd validate my_scanner/scanner.yaml
```

## Status
This is a **v0.1** proposal meant to bootstrap community discussion. PRs welcome!
