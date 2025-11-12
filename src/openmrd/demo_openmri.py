
import argparse, os, sys, json, yaml
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.openmrd.models import ScannerManifest, GradAxis, Gradients, RFChannel, RF, Magnet, Spectrometer, Console, Subsystems, Metadata

TEMPLATES = {
    "halbach_lowfield": {
        "metadata": {"name":"LF-OpenMRD-Halbach","organization":"MyLab","license":"MIT","contributors":["Researcher1", "Engineer1"],"created":"2025-08-27","description":"Low-field Halbach design"},
        "subsystems": {
            "magnet": {"type":"halbach","b0_t":0.08,"homogeneity_ppm_roi_mm":{"ppm":500,"roi_mm":120},"geometry":{},"materials":["NdFeB"],"files":{}},
            "gradients": {"form_factor":"cylindrical","axes":{
                "x":{"gmax_mTm":40,"slew_Tm_s":60,"resistance_ohm":1.2,"inductance_mH":2.8},
                "y":{"gmax_mTm":40,"slew_Tm_s":60,"resistance_ohm":1.2,"inductance_mH":2.8},
                "z":{"gmax_mTm":35,"slew_Tm_s":50,"resistance_ohm":1.5,"inductance_mH":3.1}
            }},
            "rf": {"tx":{"type":"solenoid","f0_hz":3.2e6,"q_factor":120,"impedance_ohm":50},
                   "rx":{"type":"solenoid","f0_hz":3.2e6,"q_factor":180,"impedance_ohm":50}},
            "spectrometer":{"vendor_or_open":"OpenSpecX","sampling_rate_hz":1e6,"bit_depth":16,"max_tx_freq_hz":10e6},
            "console":{"os":"Linux","api":"Python gRPC","pulseq_support":True,"latency_ms":2.5}
        }
    }
}

def init_cmd(args):
    pkg = args.package
    template = args.template
    os.makedirs(pkg, exist_ok=True)
    os.makedirs(os.path.join(pkg,"cad"), exist_ok=True)
    os.makedirs(os.path.join(pkg,"fieldmaps"), exist_ok=True)
    os.makedirs(os.path.join(pkg,"rf"), exist_ok=True)
    os.makedirs(os.path.join(pkg,"bom"), exist_ok=True)
    cfg = TEMPLATES.get(template, TEMPLATES["halbach_lowfield"])
    manifest = ScannerManifest(metadata=Metadata(**cfg["metadata"]),
                               subsystems=Subsystems(
                                   magnet=Magnet(**cfg["subsystems"]["magnet"]),
                                   gradients=Gradients(form_factor=cfg["subsystems"]["gradients"]["form_factor"],
                                                       axes={k: GradAxis(**v) for k,v in cfg["subsystems"]["gradients"]["axes"].items()}),
                                   rf=RF(tx=RFChannel(**cfg["subsystems"]["rf"]["tx"]), rx=RFChannel(**cfg["subsystems"]["rf"]["rx"])),
                                   spectrometer=Spectrometer(**cfg["subsystems"]["spectrometer"]),
                                   console=Console(**cfg["subsystems"]["console"])
                               ))
    with open(os.path.join(pkg,"scanner.yaml"),"w") as f:
        yaml.safe_dump(manifest.model_dump(), f, sort_keys=False)
    print(f"Initialized OpenMRD package at {pkg}/scanner.yaml")

def validate_cmd(args):
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
    # Initialize with default arguments
    class Args:
        package = "default_package"
        template = "halbach_lowfield"
        manifest = os.path.join(package, "scanner.yaml")
        func = None

    # First, run init_cmd
    init_args = Args()
    init_args.func = init_cmd
    init_args.func(init_args)

    # Then, run validate_cmd
    val_args = Args()
    val_args.manifest = init_args.manifest
    val_args.func = validate_cmd
    val_args.func(val_args)


if __name__ == "__main__":
    main()
