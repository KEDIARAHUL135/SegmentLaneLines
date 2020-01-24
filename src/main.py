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
import src.macros as M


################################################################################
# Function      : FindMaskImage
# Parameters    : InputImage - Holds the image to be processed.
#                 HSVImage - Holds hsv form of input image.
#                 MaskImage - Holds the image after masking.
# Description   : This function finds the mask image of the original image
#                 for yellow and white areas showing road lines. But other
#                 similar coloured objects are also included like air.
# Return        : MaskImage
################################################################################
def FindMaskImage(InputImage):
    HSVImage = cv2.cvtColor(InputImage, cv2.COLOR_BGR2HSV)
    MaskImage = cv2.inRange(HSVImage, M.LOWER_BOUND, M.UPPER_BOUND)
    cv2.imshow("Mask", MaskImage)
    return MaskImage


############################################################ ####################
# Function      : ProcessImage
# Parameters    : InputImage - Holds the image to be processed.
#                 MaskImage - Holds the image after masking.
# Description   :
# Return        :
################################################################################
def ProcessImage(InputImage):
    MaskImage = FindMaskImage(InputImage)


################################################################################
# Function      : ReadInputAndProcess
# Parameters    : InputImagesFolderPath - This contains the path of
#                                         InputImages folder
#                 ImageName - Name of image to be read
#                 InputImage - Input image to be processed
#                 KeyPressed - read the key pressed by the user
# Description   : This function reads all images present in InputImages folder
#                 one by one and passes them for processing and breaks the
#                 process when spacebar is pressed.
# Return        : -
################################################################################
def ReadInputAndProcess():
    InputImagesFolderPath = os.path.abspath(os.path.join('InputImages'))

    for ImageName in os.listdir(InputImagesFolderPath):
        InputImage = cv2.imread(InputImagesFolderPath + '/' + ImageName)
        InputImage = cv2.resize(InputImage, (842, 486))
        cv2.imshow("InputImage", InputImage)

        ProcessImage(InputImage)

        KeyPressed = cv2.waitKey(M.WAITKEY_VALUE)

        if KeyPressed == 32:      # Break when "Spacebar" is pressed
            break


ReadInputAndProcess()
