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
# Return        : Image
################################################################################
def FindLines(MaskImage, InputImage):
    # Copy original Image
    Image = InputImage.copy()

    # Find edge image and lines in the edge image.
    EdgeImage = cv2.Canny(MaskImage, 10, 10, apertureSize=3)
    Lines = cv2.HoughLinesP(EdgeImage, 1, np.pi / 180, 10, minLineLength=M.MIN_LINE_LENGTH, maxLineGap=40)

    # Run code according to the approach used.
    if M.CROP_IMAGE_or_LOWER_HALF_APPROACH == 1:        # Lower Half Approach
        # Check if no lines are found
        if Lines is not None:
            for Line in Lines:
                for x1, y1, x2, y2 in Line:
                    # Filter lines whose both ends are in the upper half of the image.
                    if y1 >= Image.shape[0]/2 and y2 >= Image.shape[0]/2:
                        # Draw line.
                        cv2.line(Image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        else:
            # Possible reason of no lines found is high value of minLineLength parameter.
            # If M.MIN_LINE_LENGTH < 0, then the lines are not found in any condition so return.
            if M.MIN_LINE_LENGTH >= 0:
                M.MIN_LINE_LENGTH -= 1
                FindLines(MaskImage, Image)
            else:
                return Image

    elif M.CROP_IMAGE_or_LOWER_HALF_APPROACH == 0:      # Crop Image Approach
        # Check if no lines are found
        if Lines is not None:
            for Line in Lines:
                for x1, y1, x2, y2 in Line:
                    # Draw Line.
                    cv2.line(Image, (x1, y1 + int(Image.shape[0]/2)),\
                             (x2, y2 + int(Image.shape[0]/2)), (0, 255, 0), 2)

        else:
            # Possible reason of no lines found is high value of minLineLength parameter.
            # If M.MIN_LINE_LENGTH < 0, then the lines are not found in any condition so return.
            if M.MIN_LINE_LENGTH >= 0:
                M.MIN_LINE_LENGTH -= 1
                FindLines(MaskImage, Image)
            else:
                return Image

    # Reset the value to original.
    M.MIN_LINE_LENGTH = M.MIN_LINE_LENGTH_FIX

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
    # Convert to HSV and apply mask
    HSVImage = cv2.cvtColor(InputImage, cv2.COLOR_BGR2HSV)
    MaskImage = cv2.inRange(HSVImage, M.LOWER_BOUND, M.UPPER_BOUND)

    # Erode the mask image
    Kernel = np.ones((3, 3), np.uint8)
    ErodedMask = cv2.erode(MaskImage, Kernel, iterations=1)

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
    # Find mask of the image for white and yellow colours.
    MaskImage = FindMaskImage(InputImage)

    # Crop image according to approach used
    if M.CROP_IMAGE_or_LOWER_HALF_APPROACH == 0:
        MaskImage = MaskImage[int(MaskImage.shape[0]/2):, :]

    LanesImage = FindLines(MaskImage, InputImage)

    cv2.imshow("InputImage", InputImage)
    cv2.imshow("LanesDetected", LanesImage)


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

    # Read input mages one by one nd passing for execution
    for ImageName in os.listdir(InputImagesFolderPath):
        InputImage = cv2.imread(InputImagesFolderPath + '/' + ImageName)
        InputImage = cv2.resize(InputImage, (842, 486))

        ProcessImage(InputImage)

        # Check waitkey value.
        KeyPressed = cv2.waitKey(M.WAITKEY_VALUE)
        if KeyPressed == 32:      # Break when "Spacebar" is pressed
            break


ReadInputAndProcess()
