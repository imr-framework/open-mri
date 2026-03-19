from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Union

# ==========================================================
# 1️⃣ Acquisition / Contrast Parameters
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

# ==========================================================
# 7️⃣ High-level MRI Reconstruction Pipeline (Updated)
# ==========================================================
class MRIPipelineExtended(BaseModel):
    contrast_settings: List[ContrastParameters]
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

# ==========================================================
# Example: Creating an extended pipeline
# ==========================================================
example_pipeline_extended = MRIPipelineExtended(
    contrast_settings=[
        ContrastParameters(name="T1", echo_time_ms=10, repetition_time_ms=500),
        ContrastParameters(name="T2", echo_time_ms=80, repetition_time_ms=3000),
        ContrastParameters(name="FLAIR", echo_time_ms=120, repetition_time_ms=9000)
    ],
    kspace_recon=KSpaceReconstruction(algorithm="FFT", filtering="Hamming"),
    classical_denoising=ClassicalDenoising(method="Gaussian", parameters={"sigma": 0.5}),
    motion_correction=MotionCorrection(method="rigid"),
    super_resolution=SuperResolution(method="DL-based", scale_factor=2.0),
    dl_reconstruction=DLReconstruction(model_name="nnUNet", checkpoint_path="/path/to/checkpoint.pth", domain_adaptation=True),
    visualization=Visualization(fusion=True, overlay_masks=True),
    evaluation=Evaluation(reference="/path/to/ref.nii", metrics=["SSIM", "PSNR", "Dice"])
)


# ✅ Key Updates / Optional Steps

# MotionCorrection – optional, can be applied before reconstruction.

# SuperResolution – optional, either classical interpolation or DL-based.

# DLReconstruction – optional, can replace or complement classical reconstruction.

# ClassicalDenoising – optional, can apply pre- or post-reconstruction.

# All steps optional – pipeline is flexible: you can run only traditional steps, only DL, or hybrid.

# Metadata / Comments – every step has comments field for reproducibility and documentation.