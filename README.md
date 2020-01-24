# SegmentLaneLines

This project aims to detect lane line on a road in a image.



### Approach

The image is masked first for yellow and white colours as lane lines of road are of these colours only. On masking, the noise like air also arises which cannot be removed by masking. After masking, the image is sent for edge detection followed by Hough Lines detection. To remove errors due to noise as mentioned earlier, two approaches are used which give almost similar result. 

First Approach - Lower Half Approach:
Lines are filtered out if both the ends of the line donot lie in the lower half of the image.

Second Approach - Crop Image Approach - 
The image passed for detection of edge is not the ful image. Instead it is the cropped image of the lower half of the original image. Due to this the lines are not detected for the sky and hence the noise is reduced.



### Bugs

Still noise is present in the bushes as their colour matches with the yellow line on the road. This bug will generally not arise in the scenario of a car moving on a city road as bushes arre not present along the city road and yellow coloured object close to ground are rare.



### Folder Structure

`src` folder contains the main source code for the project.
