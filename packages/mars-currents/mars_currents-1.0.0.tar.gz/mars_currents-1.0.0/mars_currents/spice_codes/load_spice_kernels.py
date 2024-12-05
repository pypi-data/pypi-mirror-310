import os
import spiceypy as spice
from spiceypy.utils.support_types import SpiceyError

def load_spice_kernels(kernel_path):
    if not os.path.exists(f'{kernel_path}'):
        raise IOError(f"spice kernel: {kernel_path} was not found.")
    else:
        spice.furnsh(kernel_path)
    return