"""
OpenMRD Scanner Manifest Generator (SI Units Enforced)

Generates scanner manifests for:
- C-type magnet
- H-type magnet
- Halbach magnet

Outputs:
    scanner_c_type.yaml
    scanner_h_type.yaml
    scanner_halbach.yaml
"""

import os
import sys
import yaml
from copy import deepcopy

# Add project path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.openmrd.models import *


# -------------------------
# BASE TEMPLATE (SI UNITS)
# -------------------------

BASE_TEMPLATE = {
    "metadata": {
        "name": "OpenMRD Scanner",
        "organization": "DIY MRI",
        "license": "MIT",
        "contributors": ["Researcher1", "Engineer1"],
        "created": "2026-01-01",
        "description": "Parametric MRI scanner (SI units)"
    },
    "subsystems": {
        "gradients": {
            "form_factor": "biplanar",
            "geometry": {
                "form_factor": "biplanar",
                "topology": "rectangular_loop",
                "roi_radius_m": 0.05,
                "active_length_m": 0.16,
                "plane_gap_m": 0.14,
                "plane_width_m": 0.24,
                "plane_height_m": 0.24,
                "loop_offset_m": 0.055,
                "turns": 1,
                "layers": 1,
                "segments_per_turn": 64,
                "conductor_spacing_m": 0.006,
                "return_path": "auto"
            },
            "conductor": {
                "material": "Copper",
                "conductivity_Spm": 5.8e7,
                "current_A": 10.0,
                "max_current_A": 20.0,
                "wire_radius_m": 0.003,
                "insulation_thickness_m": 0.0002
            },
            "simulation": {
                "engine": "elmerfem",
                "physics": "magnetostatic_current_density",
                "air_padding_m": 0.20,
                "mesh_min_m": 0.003,
                "mesh_max_m": 0.04,
                "boundary_condition": "magnetic_insulation",
                "result_fields": ["B", "H", "J"],
                "evaluate_roi": True
            },
            "axes": {
                "x": {
                    "gmax_Tpm": 0.025,
                    "slew_Tpm_s": 35,
                    "resistance_ohm": 2.5,
                    "inductance_H": 0.0052,
                    "target": {
                        "field_component": "Bz",
                        "gradient_axis": "x",
                        "linearity_ppm": 500,
                        "roi_radius_m": 0.05,
                        "efficiency_Tpm_per_A": 0.0025
                    },
                    "geometry": {"topology": "rectangular_loop", "loop_offset_m": 0.055}
                },
                "y": {
                    "gmax_Tpm": 0.025,
                    "slew_Tpm_s": 35,
                    "resistance_ohm": 2.5,
                    "inductance_H": 0.0052,
                    "target": {
                        "field_component": "Bz",
                        "gradient_axis": "y",
                        "linearity_ppm": 500,
                        "roi_radius_m": 0.05,
                        "efficiency_Tpm_per_A": 0.0025
                    },
                    "geometry": {"topology": "rectangular_loop", "loop_offset_m": 0.055}
                },
                "z": {
                    "gmax_Tpm": 0.020,
                    "slew_Tpm_s": 30,
                    "resistance_ohm": 3.0,
                    "inductance_H": 0.0061,
                    "target": {
                        "field_component": "Bz",
                        "gradient_axis": "z",
                        "linearity_ppm": 500,
                        "roi_radius_m": 0.05,
                        "efficiency_Tpm_per_A": 0.0020
                    },
                    "geometry": {"topology": "maxwell_pair", "loop_offset_m": 0.0}
                }
            }
        },
        "rf": {
            "tx": {"type": "solenoid", "f0_hz": 11.5e6, "q_factor": 100, "impedance_ohm": 50},
            "rx": {"type": "solenoid", "f0_hz": 11.5e6, "q_factor": 150, "impedance_ohm": 50},
            "shielding": "copper"
        },
        "spectrometer": {
            "model": "RedPitaya-122",
            "sampling_rate_hz": 122e6,
            "bit_depth": 16,
            "max_tx_freq_hz": 50e6
        },
        "console": {
            "os": "Linux",
            "api": "Python gRPC",
            "pulseq_support": True,
            "latency_ms": 3.0
        }
    }
}


def gradients_biplanar(roi_radius_m=0.05, plane_gap_m=0.14):
    cfg = deepcopy(BASE_TEMPLATE["subsystems"]["gradients"])
    cfg["form_factor"] = "biplanar"
    cfg["geometry"].update(
        {
            "form_factor": "biplanar",
            "topology": "rectangular_loop",
            "roi_radius_m": roi_radius_m,
            "plane_gap_m": plane_gap_m,
        }
    )

    for axis, ax in cfg["axes"].items():
        ax["target"]["roi_radius_m"] = roi_radius_m
        ax.setdefault("geometry", {})["form_factor"] = "biplanar"

    cfg["axes"]["z"]["geometry"]["topology"] = "maxwell_pair"
    return cfg


def gradients_cylindrical(roi_radius_m=0.05, cylinder_radius_m=0.11, cylinder_length_m=0.20):
    cfg = deepcopy(BASE_TEMPLATE["subsystems"]["gradients"])
    cfg["form_factor"] = "cylindrical"
    cfg["geometry"].update(
        {
            "form_factor": "cylindrical",
            "topology": "saddle",
            "roi_radius_m": roi_radius_m,
            "active_length_m": cylinder_length_m,
            "cylinder_radius_m": cylinder_radius_m,
            "cylinder_length_m": cylinder_length_m,
            "saddle_angle_deg": 70.0,
            "segments_per_turn": 96,
            "conductor_spacing_m": 0.006,
        }
    )

    for axis, ax in cfg["axes"].items():
        ax["target"]["roi_radius_m"] = roi_radius_m
        ax.setdefault("geometry", {})["form_factor"] = "cylindrical"
        ax["geometry"]["cylinder_radius_m"] = cylinder_radius_m
        ax["geometry"]["cylinder_length_m"] = cylinder_length_m
        ax["geometry"]["segments_per_turn"] = 96

    cfg["axes"]["x"]["geometry"]["topology"] = "saddle"
    cfg["axes"]["y"]["geometry"]["topology"] = "saddle"
    cfg["axes"]["z"]["geometry"]["topology"] = "maxwell_pair"
    cfg["axes"]["z"]["geometry"]["saddle_angle_deg"] = None
    return cfg


# -------------------------
# MAGNET CONFIGURATIONS (SI)
# -------------------------

def magnet_c_type():
    return {
        "type": "c_type",
        "b0_t": 0.35,
        "homogeneity_ppm_roi_mm": {"ppm": 200, "roi_m": 0.07},
        "geometry": {
            "m_dia": 0.2032,
            "m_thick": 0.0508,
            "pole_thick": 0.0508,
            "gap": 0.11,
            "yoke_w": 0.3,
            "yoke_t": 0.08
        }
    }


def magnet_h_type():
    return {
        "type": "h_type",
        "b0_t": 0.5,
        "homogeneity_ppm_roi_mm": {"ppm": 100, "roi_m": 0.09},
        "geometry": {
            "m_dia": 0.25,
            "m_thick": 0.06,
            "pole_thick": 0.06,
            "gap": 0.12,
            "yoke_w": 0.35,
            "yoke_t": 0.1
        }
    }


def magnet_halbach():
    return {
        "type": "halbach",
        "b0_t": 0.2,
        "homogeneity_ppm_roi_mm": {
            "ppm": 300,
            "roi_m": 0.06
        },
        "geometry": {

            # -------------------------
            # Ring lattice
            # -------------------------
            "segments": 32,          # magnets around circumference
            "rings": 24,             # axial rings
                                   # total magnets = 768

            # -------------------------
            # Bore / radius
            # -------------------------
            "bore_diameter": 0.20,   # 20 cm bore
            "ring_radius": 0.145,    # magnet center radius

            # -------------------------
            # Magnet brick size
            # -------------------------
            "magnet_width": 0.0254,   # tangential (1 in)
            "magnet_depth": 0.0254,   # radial (1 in)

            # axial size determined automatically
            "axial_mode": "auto",

            # total magnetized length
            "target_length": 0.60,    # 60 cm active length

            # inter-ring spacing
            "ring_gap": 0.001,        # 1 mm

            # fallback if explicit mode used
            "magnet_length": 0.020,

            # -------------------------
            # Advanced controls
            # -------------------------
            "ring_offsets": None,     # optional list length = rings
            "radius_taper": None,     # optional list
            "angle_error_deg": 0.0,   # manufacturing tolerance
            "remanence_T": 1.2
        }
    }
# -------------------------
# BUILD MANIFEST
# -------------------------

def build_manifest(magnet_cfg, name, gradients_cfg=None):
    cfg = deepcopy(BASE_TEMPLATE)
    gradients_cfg = gradients_cfg or cfg["subsystems"]["gradients"]

    # ---- FIX: override metadata safely ----
    metadata_dict = dict(cfg["metadata"])
    metadata_dict["name"] = name

    return ScannerManifest(
        metadata=Metadata(**metadata_dict),
        subsystems=Subsystems(
            magnet=Magnet(**magnet_cfg),
            gradients=Gradients(
                form_factor=gradients_cfg["form_factor"],
                geometry=GradientGeometry(**gradients_cfg["geometry"]),
                conductor=GradientConductor(**gradients_cfg["conductor"]),
                simulation=GradientSimulation(**gradients_cfg["simulation"]),
                axes={k: GradAxis(**v) for k, v in gradients_cfg["axes"].items()}
            ),
            rf=RF(
                tx=RFChannel(**cfg["subsystems"]["rf"]["tx"]),
                rx=RFChannel(**cfg["subsystems"]["rf"]["rx"])
            ),
            spectrometer=Spectrometer(**cfg["subsystems"]["spectrometer"]),
            console=Console(**cfg["subsystems"]["console"]),
            recon_pipeline=ReconstructionManifest(
                openmrd_version="0.1",
                metadata=Metadata(**metadata_dict),
                reconstruction_parameters={
                    "algorithm": "GRAPPA",
                    "acceleration_factor": 2
                }
            )
        )
    )


# -------------------------
# WRITE YAML
# -------------------------

def write_yaml(manifest, filename):
    with open(filename, "w") as f:
        yaml.safe_dump(manifest.model_dump(), f, sort_keys=False)


# -------------------------
# VALIDATION + SI CHECKS
# -------------------------

def validate_file(path):
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    manifest = ScannerManifest(**data)

    print(f"{path} schema valid ✅")

    # ---- SI checks ----
    m = manifest.subsystems.magnet
    g = manifest.subsystems.gradients

    assert 0 < m.b0_t < 10, "B0 must be Tesla"
    assert m.homogeneity_ppm_roi_mm.roi_m < 1.0, "ROI must be meters"

    for axis, ax in g.axes.items():
        assert ax.gmax_Tpm < 1.0, f"{axis}: gradient must be Tesla/m"
        assert ax.inductance_H < 1.0, f"{axis}: inductance must be Henry"

    print(f"{path} SI units check passed ✅")


# -------------------------
# GENERATE ALL
# -------------------------

def generate_all():
    configs = [
        (
            "scanner_c_type.yaml",
            magnet_c_type(),
            gradients_biplanar(roi_radius_m=0.05, plane_gap_m=0.14),
            "C-Type MRI"
        ),
        (
            "scanner_h_type.yaml",
            magnet_h_type(),
            gradients_biplanar(roi_radius_m=0.05, plane_gap_m=0.15),
            "H-Type MRI"
        ),
        (
            "scanner_halbach.yaml",
            magnet_halbach(),
            gradients_cylindrical(
                roi_radius_m=0.05,
                cylinder_radius_m=0.115,
                cylinder_length_m=0.60
            ),
            "Halbach MRI"
        ),
    ]

    for fname, magnet_cfg, gradients_cfg, name in configs:
        manifest = build_manifest(magnet_cfg, name, gradients_cfg)
        write_yaml(manifest, fname)
        print(f"Generated {fname}")


# -------------------------
# MAIN
# -------------------------

def main():
    print("Generating scanner configurations...\n")
    generate_all()

    print("\nValidating generated files...\n")
    for f in [
        "scanner_c_type.yaml",
        "scanner_h_type.yaml",
        "scanner_halbach.yaml"
    ]:
        validate_file(f)


if __name__ == "__main__":
    main()
