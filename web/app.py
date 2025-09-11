import streamlit as st
import yaml
import numpy as np
import matplotlib.pyplot as plt
from utils import plot_fieldmap_slice, plot_gradient_linearity

st.title("OpenMRD Manifest Preview")

uploaded = st.file_uploader("Upload an OpenMRD manifest (.yaml or .json)", type=["yaml", "json"])

if uploaded is None:
    st.info("Using bundled sample manifest.")
    with open("sample_manifest.yaml") as f:
        manifest = yaml.safe_load(f)
else:
    manifest = yaml.safe_load(uploaded)

st.subheader("Manifest Metadata")
st.json(manifest)

# Try to render fieldmap if available
if "fieldmap" in manifest.get("scanner", {}):
    fieldmap_file = manifest["scanner"]["fieldmap"]["file"]
    try:
        fieldmap = np.load(fieldmap_file)
        st.subheader("Fieldmap Preview")
        fig, ax = plt.subplots()
        im = ax.imshow(fieldmap[:, :, fieldmap.shape[2]//2], cmap="viridis")
        plt.colorbar(im, ax=ax)
        st.pyplot(fig)
    except Exception as e:
        st.warning(f"Could not load fieldmap: {e}")

st.subheader("Gradient Linearity Example")
fig2, ax2 = plt.subplots()
x = np.linspace(-1, 1, 100)
linear = x
nonlinear = x + 0.05 * np.sin(5 * np.pi * x)
ax2.plot(x, linear, label="ideal")
ax2.plot(x, nonlinear, label="actual")
ax2.legend()
st.pyplot(fig2)
