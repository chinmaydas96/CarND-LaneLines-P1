# **Finding Lane Lines on the Road** 
[![Udacity - Self-Driving Car NanoDegree](https://s3.amazonaws.com/udacity-sdc/github/shield-carnd.svg)](http://www.udacity.com/drive)

<img src="examples/laneLines_thirdPass.jpg" width="480" alt="Combined Image" />


# Installation
To create an environment for this project using Conda use the following command:

```
conda env create -f environment.yml
```

After the environment is created, it needs to be activated with the command:

```
source activate carnd
```
and open the project's notebook [P1.ipynb](P1.ipynb) inside jupyter notebook:

```
jupyter notebook P1.ipynb
```

For Running it on the terminal with pip installation.

```
pip install -r requirements.txt
```

Then run the python file
```
python P1.py
```

Overview
---

* When we drive, we use our eyes to decide where to go.  The lines on the road that show us where the lanes are act as our constant reference for where to steer the vehicle.  Naturally, one of the first things we would like to do in developing a self-driving car is to automatically detect lane lines using an algorithm.

* In this project you will detect lane lines in images using Python and OpenCV.  OpenCV means "Open-Source Computer Vision", which is a package that has many useful tools for analyzing images.  

* Main Goal of this project is to create a pipeline to detect lanelines automatically and annotated them with a solid red line.


### Main functions of the pipeline :

--- 
* Convert Color image to grayscale for easier manipulation.

* Applying Gaussian blur to smooth the edged on the image.

* Applying Canny edge detection with appropiate parameters to detect edge.

* Considering Edges in a Region Of Interest(ROI) and discard all other edges.

* Applying Hough transform to find all the lines.

* Average all left and right lane line to create a smooth line in each side and annotated them with red color.

---

First the Pipeline was tested on images contained in **test_images** folder
and store them in **test_images_output** folder.


Then the pipeline was applied on videos.







Creating a Great Writeup
---
For this project, a great writeup should provide a detailed response to the "Reflection" section of the [project rubric](https://review.udacity.com/#!/rubrics/322/view). There are three parts to the reflection:

1. Describe the pipeline

2. Identify any shortcomings

3. Suggest possible improvements

We encourage using images in your writeup to demonstrate how your pipeline works.  

All that said, please be concise!  We're not looking for you to write a book here: just a brief description.

You're not required to use markdown for your writeup.  If you use another method please just submit a pdf of your writeup. Here is a link to a [writeup template file](https://github.com/udacity/CarND-LaneLines-P1/blob/master/writeup_template.md). 



