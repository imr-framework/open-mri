"""
OpenMRD Scanner Manifest Demo - C-Type Configuration

This module demonstrates how to initialize and validate an OpenMRD scanner
configuration using a C-type permanent magnet template. It creates a complete
scanner manifest with subsystems (magnet, gradients, RF, spectrometer, console)
and validates the configuration against the simulation and data models.

Usage:
    python demo_openmri_Ctype.py

Setup Instructions:
    1. Install dependencies: pip install pyyaml pydantic
    2. Ensure src/openmrd/models.py is in the parent directories
    3. Run this script to generate a sample scanner.yaml configuration
"""

import argparse, os, sys, json, yaml
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.openmrd.models import ScannerManifest, GradAxis, Gradients, RFChannel, RF, Magnet, Spectrometer, Console, Subsystems, Metadata

TEMPLATES = {
    "c_type_permanent": {
        "metadata": {"name":"C-Type-OpenMRD","organization":"DIY MRI","license":"MIT","contributors":["Researcher1", "Engineer1"],"created":"2025-08-27","description":"C-type permanent magnet design with N52 discs"},
        "subsystems": {
            "magnet": {"type":"c_type","b0_t":0.35,"homogeneity_ppm_roi_mm":{"ppm":200,"roi_mm":100},"geometry":{"disc_diameter_inches":8,"disc_thickness_inches":2,"separation_cm":9.8},"materials":["N52 NdFeB","AISI 1018 Steel"],"files":{}},
            "gradients": {"form_factor":"biplanar","axes":{
                "x":{"gmax_mTm":25,"slew_Tm_s":35,"resistance_ohm":2.5,"inductance_mH":5.2},
                "y":{"gmax_mTm":25,"slew_Tm_s":35,"resistance_ohm":2.5,"inductance_mH":5.2},
                "z":{"gmax_mTm":20,"slew_Tm_s":30,"resistance_ohm":3.0,"inductance_mH":6.1}
            }},
            "rf": {"tx":{"type":"solenoid","f0_hz":14.9e6,"q_factor":100,"impedance_ohm":50},
                   "rx":{"type":"solenoid","f0_hz":14.9e6,"q_factor":150,"impedance_ohm":50}},
            "spectrometer":{"model":"RedPitaya-122","sampling_rate_hz":122e6,"bit_depth":16,"max_tx_freq_hz":50e6},
            "console":{"name":"mri4all","os":"Linux","api":"Python gRPC","pulseq_support":True,"latency_ms":3.0}
        }
    }
}

def init_cmd(args):
    """
    Initialize a new OpenMRD scanner package with template configuration.
    
    Creates directory structure and generates a scanner.yaml manifest file
    based on the specified template (default: c_type_permanent).
    
    Args:
        args (Args): Command arguments with:
            - package (str): Output package directory name
            - template (str): Template name from TEMPLATES dict
    
    Output:
        - Creates directories: package/cad, fieldmaps, rf, bom
        - Generates: package/scanner.yaml with YAML configuration
    """
    pkg = args.package
    template = args.template
    
    # Create package directory structure
    os.makedirs(pkg, exist_ok=True)
    os.makedirs(os.path.join(pkg,"cad"), exist_ok=True)
    os.makedirs(os.path.join(pkg,"magnet"), exist_ok=True)
    os.makedirs(os.path.join(pkg,"rf"), exist_ok=True)
    os.makedirs(os.path.join(pkg,"gradient"), exist_ok=True)
    os.makedirs(os.path.join(pkg,"iqa_experiments"), exist_ok=True)
    os.makedirs(os.path.join(pkg,"bom"), exist_ok=True)
    
    # Get template config, fallback to c_type_permanent if not found
    cfg = TEMPLATES.get(template, TEMPLATES["c_type_permanent"])
    
    # Build ScannerManifest object from template
    manifest = ScannerManifest(metadata=Metadata(**cfg["metadata"]),
                               subsystems=Subsystems(
                                   magnet=Magnet(**cfg["subsystems"]["magnet"]),
                                   gradients=Gradients(form_factor=cfg["subsystems"]["gradients"]["form_factor"],
                                                       axes={k: GradAxis(**v) for k,v in cfg["subsystems"]["gradients"]["axes"].items()}),
                                   rf=RF(tx=RFChannel(**cfg["subsystems"]["rf"]["tx"]), rx=RFChannel(**cfg["subsystems"]["rf"]["rx"])),
                                   spectrometer=Spectrometer(**cfg["subsystems"]["spectrometer"]),
                                   console=Console(**cfg["subsystems"]["console"])
                               ))
    
    # Write manifest to YAML file
    with open(os.path.join(pkg,"scanner.yaml"),"w") as f:
        yaml.safe_dump(manifest.model_dump(), f, sort_keys=False)
    print(f"Initialized OpenMRD package at {pkg}/scanner.yaml")

def validate_cmd(args):
    """
    Validate an existing scanner manifest YAML file.
    
    Loads a YAML manifest and validates it against the ScannerManifest schema.
    
    Args:
        args (Args): Command arguments with:
            - manifest (str): Path to scanner.yaml file
    
    Exits:
        0 if validation passes
        1 if validation fails with error details printed
    """
    with open(args.manifest,"r") as f:
        data = yaml.safe_load(f)
    try:
        ScannerManifest(**data)
        print("Manifest is valid ✅")
        sys.exit(0)
    except Exception as e:
        print("Validation failed ❌")
        print(e)
        sys.exit(1)

def main():
    """
    Main entry point demonstrating the full workflow.
    
    Workflow:
        1. Initialize a new package with c_type_permanent template
        2. Validate the generated scanner.yaml
    
    For production use, replace with argparse-based CLI.
    """
    # Initialize with default arguments
    class Args:
        package = "default_package"
        template = "c_type_permanent"
        manifest = os.path.join(package, "scanner.yaml")
        func = None

    # Step 1: Initialize package
    print("Step 1: Initializing package...")
    init_args = Args()
    init_args.func = init_cmd
    init_args.func(init_args)

    # Step 2: Validate manifest
    print("\nStep 2: Validating manifest...")
    val_args = Args()
    val_args.manifest = init_args.manifest
    val_args.func = validate_cmd
    val_args.func(val_args)


if __name__ == "__main__":
    main()
