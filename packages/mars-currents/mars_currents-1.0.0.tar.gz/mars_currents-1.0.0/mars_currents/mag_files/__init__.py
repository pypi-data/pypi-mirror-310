#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .create_paths import create_paths
from .load_mag_data import load_mag_data
from .mag_files_list import mag_files_list

__author__ = "Apostolos Kolokotronis"
__email__ = "apostolos.kolokotronis@irf.se"
__copyright__ = "Copyright 2020-2024"
__license__ = "MIT"
__version__ = "1.0.0"
__status__ = "Prototype"

__all__ = [
    "create_paths",
    "load_mag_data",
    "mag_files_list",
]