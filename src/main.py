###############################################################################
# File          : main.py
# Created by    : Rahul Kedia
# Created on    : 24/01/2020
# Project       : SegmentLaneLines
# Description   : This file contains the main source code for the project.
################################################################################

import cv2
import numpy as np
import os


def ReadInputAndProcess():
    InputImagesFolderPath = os.path.abspath(os.path.join('InputImages'))

    for ImagePath in os.listdir(InputImagesFolderPath):
        InputImage = cv2.imread(InputImagesFolderPath + '/' + ImagePath)
        InputImage = cv2.resize(InputImage, (842, 486))
        cv2.imshow("InputImage", InputImage)

        KeyPressed = cv2.waitKey(0)

        if KeyPressed == 32:      # Break when "Spacebar" is pressed
            break


ReadInputAndProcess()
