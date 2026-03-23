
from pydantic import BaseModel, Field, RootModel
from typing import List, Optional, Union, Dict
from src.openmrd.reconstruction import *

class Homog(BaseModel):
    ppm: float
    roi_mm: float

class Magnet(BaseModel):
    type: str
    b0_t: float
    homogeneity_ppm_roi_mm: Homog
    shim_order_supported: Optional[int] = 0
    geometry: Dict[str, float] = Field(default_factory=dict)
    materials: List[str] = Field(default_factory=list)
    files: Dict[str, Union[str, List[str]]] = Field(default_factory=dict)

class GradAxis(BaseModel):
    gmax_mTm: float
    slew_Tm_s: float
    resistance_ohm: float
    inductance_mH: float
    cooling: Optional[str] = "air"
    dqdt_limits_T_s: Optional[float] = None
    files: Dict[str, List[str]] = Field(default_factory=dict)

class Gradients(BaseModel):
    form_factor: str
    axes: Dict[str, GradAxis]
    files: Dict[str, List[str]] = Field(default_factory=dict)

class RFChannel(BaseModel):
    type: str
    f0_hz: float
    q_factor: float
    impedance_ohm: float
    pmax_w: Optional[float] = None
    s_params_file: Optional[str] = None
    match_network: Optional[str] = None
    files: Dict[str, List[str]] = Field(default_factory=dict)

class RF(BaseModel):
    tx: RFChannel
    rx: Union[RFChannel, List[RFChannel]]
    shielding: Optional[str] = None

class Spectrometer(BaseModel):
    model: str
    sampling_rate_hz: float
    bit_depth: int
    max_tx_freq_hz: float
    files: Dict[str, List[str]] = Field(default_factory=dict)

class Console(BaseModel):
    os: str
    api: str
    pulseq_support: bool = True
    latency_ms: Optional[float] = None

class Metadata(BaseModel):
    name: str
    organization: str
    license: str
    contributors: List[str]
    created: str
    description: Optional[str] = None
    links: Optional[List[str]] = None
    pulseq_compatibility: Optional[str] = None

class CoordinateSystem(BaseModel):
    convention: str = "RAS"
    units: str = "SI"
    scanner_to_lab_transform: List[float] = Field(default_factory=lambda: [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1])

# ==========================================================
# 1️⃣ Acquisition / Contrast Parameters reconstruction and acquision
# ==========================================================


class ContrastParameters(BaseModel):
    name: str  # T1, T2, FLAIR, Diffusion, etc.
    echo_time_ms: Optional[float] = None
    repetition_time_ms: Optional[float] = None
    flip_angle_deg: Optional[float] = None
    b_value: Optional[float] = None  # For diffusion
    diffusion_directions: Optional[int] = None
    orientation: List[str] = Field(default_factory=lambda: ["axial", "coronal", "sagittal"])
    notes: Optional[str] = None  # Acquisition-specific info

# ==========================================================
# 2️⃣ K-space / Reconstruction Parameters (Traditional)
# ==========================================================
class KSpaceReconstruction(BaseModel):
    algorithm: str = "FFT"  # FFT, NUFFT, SENSE, GRAPPA, etc.
    filtering: Optional[str] = None  # Hamming, Gaussian, etc.
    density_compensation: Optional[bool] = False
    oversampling_factor: Optional[float] = 1.0
    orientation_correction: Optional[bool] = True  # Rotate to canonical axes
    comments: Optional[str] = "Traditional k-space reconstruction settings"

# ==========================================================
# 3️⃣ Classical Denoising / Preprocessing
# ==========================================================
class ClassicalDenoising(BaseModel):
    method: str  # Gaussian, Median, NLM, BM3D
    parameters: Dict[str, float] = Field(default_factory=dict)
    apply_before_reconstruction: Optional[bool] = True
    comments: Optional[str] = "Optional classical denoising step"

# ==========================================================
# 3.1 Motion Correction (Optional)
# ==========================================================
class MotionCorrection(BaseModel):
    method: str  # e.g., rigid, affine, non-rigid
    parameters: Dict[str, float] = Field(default_factory=dict)
    apply_before_reconstruction: Optional[bool] = True
    comments: Optional[str] = "Optional motion correction step"

# ==========================================================
# 3.2 Super-resolution (Optional)
# ==========================================================
class SuperResolution(BaseModel):
    method: str  # e.g., interpolation, DL-based
    scale_factor: Optional[float] = 2.0
    comments: Optional[str] = "Optional super-resolution enhancement"

# ==========================================================
# 4️⃣ Deep Learning Based Reconstruction
# ==========================================================
class DLReconstruction(BaseModel):
    model_name: str  # nnUNet, UNet, SwinUNet
    checkpoint_path: Optional[str] = None
    input_type: str = "k-space"  # raw or magnitude
    output_type: str = "image"
    normalization: Optional[str] = "z-score"
    augmentation: Optional[Dict[str, Union[bool, float]]] = None
    domain_adaptation: Optional[bool] = False
    comments: Optional[str] = "DL-based reconstruction and denoising"

# ==========================================================
# 5️⃣ Post-processing / Visualization
# ==========================================================
class Visualization(BaseModel):
    views: List[str] = Field(default_factory=lambda: ["axial", "coronal", "sagittal"])
    fusion: Optional[bool] = False  # Combine multiple contrasts
    overlay_masks: Optional[bool] = False  # Segmentation overlay
    windowing: Optional[Dict[str, float]] = None  # Window/level
    colormap: Optional[str] = "gray"
    comments: Optional[str] = "Visualization and multi-orientation display"

# ==========================================================
# 6️⃣ Evaluation / Metrics
# ==========================================================
class Evaluation(BaseModel):
    reference: Optional[str] = None  # Ground truth / baseline
    metrics: List[str] = Field(default_factory=lambda: ["SSIM", "PSNR", "Dice"])
    segmentation: Optional[Dict[str, str]] = None  # Mask files for evaluation
    comments: Optional[str] = "Evaluation of image quality and/or segmentation"


class ReconstructionManifest(BaseModel):
    openmrd_version: str = "0.1"
    metadata: Metadata
    coordinate_system: CoordinateSystem = CoordinateSystem()
    
    contrast_settings: List[ContrastParameters]

    reconstruction_parameters: dict
    # Traditional reconstruction steps
    kspace_recon: Optional[KSpaceReconstruction] = None
    classical_denoising: Optional[ClassicalDenoising] = None
    motion_correction: Optional[MotionCorrection] = None
    super_resolution: Optional[SuperResolution] = None
    # DL-based steps
    dl_reconstruction: Optional[DLReconstruction] = None
    # Visualization & evaluation
    visualization: Optional[Visualization] = None
    evaluation: Optional[Evaluation] = None
    notes: Optional[str] = "High-level MRI pipeline supporting both traditional and DL workflows"

    testing: Optional[dict] = None
    security: Optional[dict] = None
    checksums: Optional[List[dict]] = None
    extensions: Optional[dict] = None

class Subsystems(BaseModel):
    magnet: Magnet
    passive_shims: Optional[dict] = None
    resistive_shims: Optional[dict] = None
    gradients: Gradients
    rf: RF
    spectrometer: Spectrometer
    console: Console
    recon_pipeline: ReconstructionManifest

class ScannerManifest(BaseModel):
    openmrd_version: str = "0.1"
    metadata: Metadata
    coordinate_system: CoordinateSystem = CoordinateSystem()
    subsystems: Subsystems
    testing: Optional[dict] = None
    security: Optional[dict] = None
    checksums: Optional[List[dict]] = None
    extensions: Optional[dict] = None