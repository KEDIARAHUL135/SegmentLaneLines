###############################################################################
# File          : macros.py
# Created by    : Rahul Kedia
# Created on    : 24/01/2020
# Project       : SegmentLaneLines
# Description   : This file contains the variables/macros for main.py.
################################################################################

import numpy as np


# WaitKey value
WAITKEY_VALUE = 0


# Lower and upper bounds for masking
LOWER_BOUND = np.array([0, 0, 180])
UPPER_BOUND = np.array([255, 255, 255])