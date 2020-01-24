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
# Function      : FindLines
# Parameters    : Image - Holds the image to be processed on which lines
#                         will be drawn.
#                 EdgeImage - Holds Edge image of MaskImage
#                 MaskImage - Holds the input image after masking.
#                 Lines - Holds the list of lines found.
# Description   : This function finds the mask image of the original image
#                 for yellow and white areas showing road lines. But other
#                 similar coloured objects are also included like air.
# Return        : MaskImage
################################################################################
def FindLines(MaskImage, Image):
    EdgeImage = cv2.Canny(MaskImage, 10, 10, apertureSize=3)
    Lines = cv2.HoughLinesP(EdgeImage, 1, np.pi / 180, 10, minLineLength=M.MIN_LINE_LENGTH, maxLineGap=40)

    if Lines is not None:
        for Line in Lines:
            for x1, y1, x2, y2 in Line:
                if y1 >= Image.shape[0]/2 and y2 >= Image.shape[0]/2:
                    cv2.line(Image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    else:
        M.MIN_LINE_LENGTH -= 1
        FindLines(MaskImage, Image)

    M.MIN_LINE_LENGTH = M.MIN_LINE_LENGTH_FIX

    cv2.imshow("EdgeImage", EdgeImage)
    cv2.imshow("RoadLanes", Image)
    return Image


################################################################################
# Function      : FindMaskImage
# Parameters    : InputImage - Holds the image to be processed.
#                 HSVImage - Holds hsv form of input image.
#                 MaskImage - Holds the image after masking.
#                 Kernel - kernel used for erosion.
#                 ErodedMask - Hold the eroded mask image.
# Description   : This function finds the mask image of the original image
#                 for yellow and white areas showing road lines. But other
#                 similar coloured objects are also included like air.
# Return        : ErodedMask
################################################################################
def FindMaskImage(InputImage):

    HSVImage = cv2.cvtColor(InputImage, cv2.COLOR_BGR2HSV)
    MaskImage = cv2.inRange(HSVImage, M.LOWER_BOUND, M.UPPER_BOUND)
    Kernel = np.ones((3, 3), np.uint8)
    ErodedMask = cv2.erode(MaskImage, Kernel, iterations=1)
    cv2.imshow("Mask", ErodedMask)
    return ErodedMask


################################################################################
# Function      : ProcessImage
# Parameters    : InputImage - Holds the image to be processed.
#                 MaskImage - Holds the image after masking.
#                 LanesImage - Holds the image with lanes found.
# Description   :
# Return        :
################################################################################
def ProcessImage(InputImage):
    MaskImage = FindMaskImage(InputImage)
    LanesImage = FindLines(MaskImage, InputImage)


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
