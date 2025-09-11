import numpy as np
import matplotlib.pyplot as plt

def plot_fieldmap_slice(fieldmap, z_index=None):
    if z_index is None:
        z_index = fieldmap.shape[2] // 2
    plt.imshow(fieldmap[:, :, z_index], cmap='viridis')
    plt.colorbar(label='Hz offset')
    plt.title(f'Fieldmap slice z={z_index}')
    return plt

def plot_gradient_linearity():
    x = np.linspace(-1, 1, 100)
    linear = x
    nonlinear = x + 0.05 * np.sin(5 * np.pi * x)
    plt.plot(x, linear, label="ideal")
    plt.plot(x, nonlinear, label="actual")
    plt.legend()
    plt.title("Gradient linearity (example)")
    return plt
