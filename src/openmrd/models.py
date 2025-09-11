
from pydantic import BaseModel, Field, RootModel
from typing import List, Optional, Union, Dict

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
    vendor_or_open: str
    sampling_rate_hz: float
    bit_depth: int
    max_tx_freq_hz: float
    files: Dict[str, List[str]] = Field(default_factory=dict)

class Console(BaseModel):
    os: str
    api: str
    pulseq_support: bool = True
    latency_ms: Optional[float] = None

class Subsystems(BaseModel):
    magnet: Magnet
    passive_shims: Optional[dict] = None
    resistive_shims: Optional[dict] = None
    gradients: Gradients
    rf: RF
    spectrometer: Spectrometer
    console: Console

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

class ScannerManifest(BaseModel):
    openmrd_version: str = "0.1"
    metadata: Metadata
    coordinate_system: CoordinateSystem = CoordinateSystem()
    subsystems: Subsystems
    testing: Optional[dict] = None
    security: Optional[dict] = None
    checksums: Optional[List[dict]] = None
    extensions: Optional[dict] = None
