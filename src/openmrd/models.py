from pydantic import BaseModel, Field, validator
from typing import List, Optional, Union, Dict, Literal, Any


# -------------------------
# CORE TYPES (SI ENFORCED)
# -------------------------

class Homog(BaseModel):
    ppm: float
    roi_m: float  # meters (NOT mm)

    @validator("roi_m")
    def check_roi(cls, v):
        assert 0 < v < 1.0, "ROI must be in meters"
        return v


# -------------------------
# MAGNETIZATION
# -------------------------

class Magnetization(BaseModel):
    direction: List[float] = Field(default_factory=lambda: [0.0, 0.0, 1.0])
    magnitude: float = 1.154e6  # A/m

    @validator("magnitude")
    def check_mag(cls, v):
        assert 1e5 < v < 2e6
        return v


# -------------------------
# GEOMETRIES
# -------------------------

class CTypeGeometry(BaseModel):
    m_dia: float
    m_thick: float
    pole_thick: float
    gap: float
    yoke_w: float
    yoke_t: float

    @validator("*")
    def check_lengths(cls, v):
        assert 0 < v < 10
        return v


class HTypeGeometry(CTypeGeometry):
    pass


# -------------------------
# HALBACH (FIXED + EXTENDED)
# -------------------------

class HalbachGeometry(BaseModel):
    # block dimensions (SI)
    m_dia: float          # radial thickness
    m_thick: float        # axial length
    gap: float            # bore diameter

    # array structure
    segments: int = 32    # magnets per ring
    rings: int = 1        # number of axial rings

    # spacing model (NEW but safe defaults)
    ring_spacing: Optional[float] = 0.0
    axial_pitch: Optional[float] = None

    # layout tuning
    packing_factor: float = 0.90
    axial_mode: Literal["auto", "stacked", "shifted"] = "auto"

    @validator("segments")
    def check_segments(cls, v):
        assert v >= 4
        return v

    @validator("rings")
    def check_rings(cls, v):
        assert v >= 1
        return v

    @validator("m_dia", "m_thick", "gap")
    def check_geom(cls, v):
        assert v > 0
        return v


# -------------------------
# MAGNET (CRITICAL FIX HERE)
# -------------------------

class Magnet(BaseModel):
    type: Literal["c_type", "h_type", "halbach", "custom"]

    b0_t: float
    homogeneity_ppm_roi_mm: Homog
    shim_order_supported: Optional[int] = 0

    geometry: Union[
        CTypeGeometry,
        HTypeGeometry,
        HalbachGeometry,
        Dict[str, Any]   # IMPORTANT FIX
    ] = Field(default_factory=dict)

    materials: List[str] = Field(default_factory=lambda: [
        "Air",
        "Permanent_Magnet",
        "Steel_1018"
    ])

    magnetization: Magnetization = Field(default_factory=Magnetization)

    files: Dict[str, Union[str, List[str]]] = Field(default_factory=dict)

    @validator("b0_t")
    def check_b0(cls, v):
        assert 0 < v < 10
        return v

    def geometry_dict(self):
        if hasattr(self.geometry, "model_dump"):
            return self.geometry.model_dump()
        return self.geometry


# -------------------------
# GRADIENTS
# -------------------------

class GradientGeometry(BaseModel):
    form_factor: Literal["biplanar", "planar", "cylindrical"] = "biplanar"
    topology: Literal[
        "rectangular_loop",
        "maxwell_pair",
        "saddle",
        "stream_function",
        "custom"
    ] = "rectangular_loop"

    roi_radius_m: float = 0.05
    active_length_m: Optional[float] = None

    # Biplanar dimensions
    plane_gap_m: Optional[float] = 0.14
    plane_width_m: Optional[float] = 0.24
    plane_height_m: Optional[float] = 0.24
    loop_offset_m: Optional[float] = 0.055

    # Cylindrical dimensions
    cylinder_radius_m: Optional[float] = None
    cylinder_length_m: Optional[float] = None
    saddle_angle_deg: Optional[float] = 70.0

    # Discretization / winding construction
    turns: int = 1
    layers: int = 1
    segments_per_turn: int = 64
    conductor_spacing_m: Optional[float] = None
    return_path: Literal["auto", "outer_edge", "twisted_pair", "external"] = "auto"

    @validator("roi_radius_m")
    def check_roi_radius(cls, v):
        assert 0 < v < 1.0
        return v

    @validator("turns", "layers", "segments_per_turn")
    def check_positive_ints(cls, v):
        assert v >= 1
        return v


class GradientConductor(BaseModel):
    material: str = "Copper"
    conductivity_Spm: float = 5.8e7
    current_A: float = 10.0
    max_current_A: Optional[float] = 20.0
    voltage_limit_V: Optional[float] = None
    wire_radius_m: Optional[float] = 0.003
    trace_width_m: Optional[float] = None
    trace_thickness_m: Optional[float] = None
    insulation_thickness_m: Optional[float] = 0.0002

    @validator("conductivity_Spm", "current_A")
    def check_positive(cls, v):
        assert v > 0
        return v


class GradientTarget(BaseModel):
    field_component: Literal["Bx", "By", "Bz"] = "Bz"
    gradient_axis: Literal["x", "y", "z"]
    linearity_ppm: Optional[float] = 500.0
    roi_radius_m: float = 0.05
    efficiency_Tpm_per_A: Optional[float] = None

    @validator("roi_radius_m")
    def check_roi_radius(cls, v):
        assert 0 < v < 1.0
        return v


class GradientSimulation(BaseModel):
    engine: Literal["elmerfem", "biot_savart", "both"] = "elmerfem"
    physics: Literal["magnetostatic_current_density"] = "magnetostatic_current_density"
    air_padding_m: float = 0.20
    mesh_min_m: float = 0.003
    mesh_max_m: float = 0.04
    boundary_condition: Literal["magnetic_insulation", "infinite_box"] = "magnetic_insulation"
    result_fields: List[str] = Field(default_factory=lambda: ["B", "H", "J"])
    evaluate_roi: bool = True

    @validator("air_padding_m", "mesh_min_m", "mesh_max_m")
    def check_mesh_lengths(cls, v):
        assert v > 0
        return v


class GradAxis(BaseModel):
    gmax_Tpm: float
    slew_Tpm_s: float
    resistance_ohm: float
    inductance_H: float

    cooling: Optional[str] = "air"
    dqdt_limits_T_s: Optional[float] = None
    target: Optional[GradientTarget] = None
    geometry: Optional[GradientGeometry] = None
    conductor: GradientConductor = Field(default_factory=GradientConductor)
    simulation: GradientSimulation = Field(default_factory=GradientSimulation)
    files: Dict[str, List[str]] = Field(default_factory=dict)

    @validator("gmax_Tpm", "slew_Tpm_s", "resistance_ohm", "inductance_H")
    def check_axis_values(cls, v):
        assert v > 0
        return v


class Gradients(BaseModel):
    form_factor: Literal["biplanar", "planar", "cylindrical"]
    axes: Dict[str, GradAxis]
    geometry: Optional[GradientGeometry] = None
    conductor: GradientConductor = Field(default_factory=GradientConductor)
    simulation: GradientSimulation = Field(default_factory=GradientSimulation)
    files: Dict[str, List[str]] = Field(default_factory=dict)


# -------------------------
# RF
# -------------------------

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


# -------------------------
# OTHER SUBSYSTEMS
# -------------------------

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


class CoordinateSystem(BaseModel):
    convention: str = "RAS"
    units: str = "SI"
    scanner_to_lab_transform: List[float] = Field(
        default_factory=lambda: [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]
    )


class ReconstructionManifest(BaseModel):
    openmrd_version: str = "0.1"
    metadata: Metadata
    coordinate_system: CoordinateSystem = CoordinateSystem()
    reconstruction_parameters: dict


class Subsystems(BaseModel):
    magnet: Magnet
    gradients: Gradients
    rf: RF
    spectrometer: Spectrometer
    console: Console
    recon_pipeline: Optional[ReconstructionManifest] = None


class ScannerManifest(BaseModel):
    openmrd_version: str = "0.1"
    metadata: Metadata
    coordinate_system: CoordinateSystem = CoordinateSystem()
    subsystems: Subsystems

