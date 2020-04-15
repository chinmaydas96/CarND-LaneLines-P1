#!/usr/bin/env python
# coding: utf-8

# # Self-Driving Car Engineer Nanodegree
# 
# 
# ## Project: **Finding Lane Lines on the Road** 
# ***
# In this project, you will use the tools you learned about in the lesson to identify lane lines on the road.  You can develop your pipeline on a series of individual images, and later apply the result to a video stream (really just a series of images). Check out the video clip "raw-lines-example.mp4" (also contained in this repository) to see what the output should look like after using the helper functions below. 
# 
# Once you have a result that looks roughly like "raw-lines-example.mp4", you'll need to get creative and try to average and/or extrapolate the line segments you've detected to map out the full extent of the lane lines.  You can see an example of the result you're going for in the video "P1_example.mp4".  Ultimately, you would like to draw just one line for the left side of the lane, and one for the right.
# 
# In addition to implementing code, there is a brief writeup to complete. The writeup should be completed in a separate file, which can be either a markdown file or a pdf document. There is a [write up template](https://github.com/udacity/CarND-LaneLines-P1/blob/master/writeup_template.md) that can be used to guide the writing process. Completing both the code in the Ipython notebook and the writeup template will cover all of the [rubric points](https://review.udacity.com/#!/rubrics/322/view) for this project.
# 
# ---
# Let's have a look at our first image called 'test_images/solidWhiteRight.jpg'.  Run the 2 cells below (hit Shift-Enter or the "play" button above) to display the image.
# 
# **Note: If, at any point, you encounter frozen display windows or other confounding issues, you can always start again with a clean slate by going to the "Kernel" menu above and selecting "Restart & Clear Output".**
# 
# ---

# **The tools you have are color selection, region of interest selection, grayscaling, Gaussian smoothing, Canny Edge Detection and Hough Tranform line detection.  You  are also free to explore and try other techniques that were not presented in the lesson.  Your goal is piece together a pipeline to detect the line segments in the image, then average/extrapolate them and draw them onto the image for display (as below).  Once you have a working pipeline, try it out on the video stream below.**
# 
# ---
# 
# <figure>
#  <img src="examples/line-segments-example.jpg" width="380" alt="Combined Image" />
#  <figcaption>
#  <p></p> 
#  <p style="text-align: center;"> Your output should look something like this (above) after detecting line segments using the helper functions below </p> 
#  </figcaption>
# </figure>
#  <p></p> 
# <figure>
#  <img src="examples/laneLines_thirdPass.jpg" width="380" alt="Combined Image" />
#  <figcaption>
#  <p></p> 
#  <p style="text-align: center;"> Your goal is to connect/average/extrapolate line segments to get output like this</p> 
#  </figcaption>
# </figure>

# **Run the cell below to import some packages.  If you get an `import error` for a package you've already installed, try changing your kernel (select the Kernel menu above --> Change Kernel).  Still have problems?  Try relaunching Jupyter Notebook from the terminal prompt.  Also, consult the forums for more troubleshooting tips.**  

# ## Import Packages

# In[1]:


#importing some useful packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2


# ## Read in an Image

# In[2]:


#reading in an image
image = mpimg.imread('test_images/solidWhiteRight.jpg')

#printing out some stats and plotting
print('This image is:', type(image), 'with dimensions:', image.shape)
plt.imshow(image)  # if you wanted to show a single color channel image called 'gray', for example, call as plt.imshow(gray, cmap='gray')


# ## Ideas for Lane Detection Pipeline

# **Some OpenCV functions (beyond those introduced in the lesson) that might be useful for this project are:**
# 
# `cv2.inRange()` for color selection  
# `cv2.fillPoly()` for regions selection  
# `cv2.line()` to draw lines on an image given endpoints  
# `cv2.addWeighted()` to coadd / overlay two images  
# `cv2.cvtColor()` to grayscale or change color  
# `cv2.imwrite()` to output images to file  
# `cv2.bitwise_and()` to apply a mask to an image
# 
# **Check out the OpenCV documentation to learn about these and discover even more awesome functionality!**

# ## Helper Functions

# Below are some helper functions to help get you started. They should look familiar from the lesson!

# In[3]:


import math

def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    """
    Applies an image mask.
    
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    `vertices` should be a numpy array of integer points.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

            
            
def draw_lines_new(img, lines, color=[255, 0, 0], thickness=6):
    """
    NOTE: this is the function you might want to use as a starting point once you want to 
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).  
    
    Think about things like separating line segments by their 
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of 
    the lines and extrapolate to the top and bottom of the lane.
    
    This function draws `lines` with `color` and `thickness`.    
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """
    ## create an empty array with all the line slope
    all_slopes = np.zeros((len(lines)))
    
    ## create an empty array for left lines
    left_line_slope = []
    
    ## create an empty array for right lines
    right_line_slope = []
    
    # keep each line slope in the array
    for index,line in enumerate(lines):
        for x1,y1,x2,y2 in line: 
            all_slopes[index] =  (y2-y1)/(x2-x1)
    
    # get all left line slope if it is positive
    left_line_slope = all_slopes[all_slopes > 0]
    
    # get all left line slope if it is negetive
    right_line_slope = all_slopes[all_slopes < 0]
    
    ## mean value of left slope and right slope
    m_l = left_line_slope.mean()
    m_r = right_line_slope.mean()
    
    
    # Create empty list for all the left points and right points
    final_x4_l = []
    final_x3_l = []
    
    final_x4_r = []
    final_x3_r = []
    
    ## get fixed y-cordinate in both top and bottom point
    y4 = 320
    y3 = img.shape[0]
    
    ## Go for each line to calculate left top x-cordinate, right top x-cordinate,
    ##                               left buttom x-cordinate, right bottom top x-cordinate 
    for index,line in enumerate(lines):
        for x1,y1,x2,y2 in line:  
            
            m = (y2-y1)/(x2-x1)    
            
            if m > 0 :
                final_x4_l.append(int(((x1 + (y4  - y1) / m_l) + (x2 + (y4  - y2) / m_l))/ 2))
                final_x3_l.append(int(((x1 + (y3  - y1) / m_l) + (x2 + (y3  - y2) / m_l))/ 2))       
            else:                   
                final_x4_r.append(int(((x1 + (y4  - y1) / m_r) + (x2 + (y4  - y2) / m_r))/ 2))
                final_x3_r.append(int(((x1 + (y3  - y1) / m_r) + (x2 + (y3  - y2) / m_r))/ 2))
                
                
    try :
        ## taking average of each points
        x4_l = int(sum(final_x4_l)/ len(final_x4_l))
        x4_r = int(sum(final_x4_r)/ len(final_x4_r))

        x3_l = int(sum(final_x3_l)/ len(final_x3_l))
        x3_r = int(sum(final_x3_r)/ len(final_x3_r))    
        
        ## Draw the left line and right line
        cv2.line(img, (x4_l, y4), (x3_l, y3), color, thickness)  
        cv2.line(img, (x4_r, y4), (x3_r, y3), color, thickness)  
    except:
        pass


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.
        
    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines_new(line_img, lines)
    return line_img

# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, α=0.8, β=1., γ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.
    
    `initial_img` should be the image before any processing.
    
    The result image is computed as follows:
    
    initial_img * α + img * β + γ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, γ)


# ## Test Images
# 
# Build your pipeline to work on the images in the directory "test_images"  
# **You should make sure your pipeline works well on these images before you try the videos.**

# In[4]:


import os
os.listdir("test_images/")


# ## Build a Lane Finding Pipeline
# 
# 

# Build the pipeline and run your solution on all test_images. Make copies into the `test_images_output` directory, and you can use the images in your writeup report.
# 
# Try tuning the various parameters, especially the low and high Canny thresholds as well as the Hough lines parameters.

# In[18]:


# TODO: Build your pipeline that will draw lane lines on the test_images
# then save them to the test_images_output directory.

def preprocess_image(image_path):

    image = mpimg.imread(image_path)
    gray_image = grayscale(image)
    blured_image = gaussian_blur(gray_image, 5)
    canny_image = canny(gray_image, low_threshold=100, high_threshold=170)
    vertices = np.array([[(80,image.shape[0]),(450, 320), (490, 320), (image.shape[1],image.shape[0])]], dtype=np.int32)
    roi_image = region_of_interest(canny_image, vertices)
    hough_img = hough_lines(roi_image, rho=2, theta=np.pi/180, threshold=50, min_line_len=100, max_line_gap=160)
    final_img= weighted_img(hough_img, image, α=0.8, β=1., γ=0.)
    return final_img



def process_test_images(source_folder,destination_folder):
    
    
    ## create destination folder if not present
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    ## Get all input files from the source folder
    list_test_files = os.listdir(source_folder)
    
    ## process all the input files
    for file in list_test_files:
        output = preprocess_image(source_folder+ '/' + file)
        cv2.imwrite(destination_folder+'/'+ file, cv2.cvtColor(output, cv2.COLOR_RGB2BGR))
            
    
    
process_test_images('test_images','test_images_output')


# In[19]:




# In[20]:


os.listdir('test_images')


# In[21]:


# Checking in an image
plt.figure(figsize=(15,8))
plt.subplot(121)
image = mpimg.imread('test_images/solidYellowCurve.jpg')
plt.imshow(image)
plt.title('Original image')

plt.subplot(122)
image = mpimg.imread('test_images_output/whiteCarLaneSwitch.jpg')
plt.imshow(image)
plt.title('Output image')
plt.show()


# ## Test on Videos
# 
# You know what's cooler than drawing lanes over images? Drawing lanes over video!
# 
# We can test our solution on two provided videos:
# 
# `solidWhiteRight.mp4`
# 
# `solidYellowLeft.mp4`
# 
# **Note: if you get an import error when you run the next cell, try changing your kernel (select the Kernel menu above --> Change Kernel). Still have problems? Try relaunching Jupyter Notebook from the terminal prompt. Also, consult the forums for more troubleshooting tips.**
# 
# **If you get an error that looks like this:**
# ```
# NeedDownloadError: Need ffmpeg exe. 
# You can download it by calling: 
# imageio.plugins.ffmpeg.download()
# ```
# **Follow the instructions in the error message and check out [this forum post](https://discussions.udacity.com/t/project-error-of-test-on-videos/274082) for more troubleshooting tips across operating systems.**

# In[9]:


# Import everything needed to edit/save/watch video clips
from moviepy.editor import VideoFileClip


# In[10]:


def process_image(image):
    # NOTE: The output you return should be a color image (3 channel) for processing video below
    # TODO: put your pipeline here,
    # you should return the final output (image where lines are drawn on lanes)
    
    gray_image = grayscale(image)
    blured_image = gaussian_blur(gray_image, 5)
    canny_image = canny(gray_image, low_threshold=100, high_threshold=170)
    vertices = np.array([[(80,image.shape[0]),(450, 320), (490, 320), (image.shape[1],image.shape[0])]], dtype=np.int32)
    roi_image = region_of_interest(canny_image, vertices)
    hough_img = hough_lines(roi_image, rho=2, theta=np.pi/180, threshold=50, min_line_len=100, max_line_gap=160)
    result= weighted_img(hough_img, image, α=0.8, β=1., γ=0.)
    
    return result


# Let's try the one with the solid white lane on the right first ...

# In[11]:


white_output = 'test_videos_output/solidWhiteRight.mp4'
## To speed up the testing process you may want to try your pipeline on a shorter subclip of the video
## To do so add .subclip(start_second,end_second) to the end of the line below
## Where start_second and end_second are integer values representing the start and end of the subclip
## You may also uncomment the following line for a subclip of the first 5 seconds
##clip1 = VideoFileClip("test_videos/solidWhiteRight.mp4").subclip(0,5)
clip1 = VideoFileClip("test_videos/solidWhiteRight.mp4")
white_clip = clip1.fl_image(process_image) #NOTE: this function expects color images!!
white_clip.write_videofile(white_output, audio=False)



# ## Improve the draw_lines() function
# 
# **At this point, if you were successful with making the pipeline and tuning parameters, you probably have the Hough line segments drawn onto the road, but what about identifying the full extent of the lane and marking it clearly as in the example video (P1_example.mp4)?  Think about defining a line to run the full length of the visible lane based on the line segments you identified with the Hough Transform. As mentioned previously, try to average and/or extrapolate the line segments you've detected to map out the full extent of the lane lines. You can see an example of the result you're going for in the video "P1_example.mp4".**
# 
# **Go back and modify your draw_lines function accordingly and try re-running your pipeline. The new output should draw a single, solid line over the left lane line and a single, solid line over the right lane line. The lines should start from the bottom of the image and extend out to the top of the region of interest.**

# Now for the one with the solid yellow lane on the left. This one's more tricky!

# In[13]:


yellow_output = 'test_videos_output/solidYellowLeft.mp4'
## To speed up the testing process you may want to try your pipeline on a shorter subclip of the video
## To do so add .subclip(start_second,end_second) to the end of the line below
## Where start_second and end_second are integer values representing the start and end of the subclip
## You may also uncomment the following line for a subclip of the first 5 seconds
##clip2 = VideoFileClip('test_videos/solidYellowLeft.mp4').subclip(0,5)
clip2 = VideoFileClip('test_videos/solidYellowLeft.mp4')
yellow_clip = clip2.fl_image(process_image)
yellow_clip.write_videofile(yellow_output, audio=False)



def process_image(image):
    # NOTE: The output you return should be a color image (3 channel) for processing video below
    # TODO: put your pipeline here,
    # you should return the final output (image where lines are drawn on lanes)
    cv2.imwrite('image_test.jpg',image)
    gray_image = grayscale(image)
    blured_image = gaussian_blur(gray_image, 5)
    canny_image = canny(gray_image, low_threshold=100, high_threshold=170)
    cv2.imwrite('image_test_canny.jpg',canny_image)
    x_size = image.shape[1]
    y_size = image.shape[0]
    left_bottom = (80, y_size)
    left_top = (x_size / 2 - 50, y_size / 2 + 50)
    right_bottom = (x_size - 80, y_size)
    right_top = (x_size / 2 + 50, y_size / 2 + 50)
    #vertices = np.array([[left_bottom, left_top, right_top, right_bottom]], dtype=np.int32)
    
    
    #vertices = np.array([[(280,image.shape[0]),(450, 320), (490, 320), (image.shape[1],image.shape[0])]], dtype=np.int32)
    vertices = np.array([[(300,680),(620, 460), (720, 460), (1085,673)]], dtype=np.int32)
    roi_image = region_of_interest(canny_image, vertices)
    try:
        hough_img = hough_lines(roi_image, rho=2, theta=np.pi/180, threshold=50, min_line_len=100, max_line_gap=160)
        result= weighted_img(hough_img, image, α=0.8, β=1., γ=0.)
        return result
    except:
        return image


# In[16]:


challenge_output = 'test_videos_output/challenge.mp4'
## To speed up the testing process you may want to try your pipeline on a shorter subclip of the video
## To do so add .subclip(start_second,end_second) to the end of the line below
## Where start_second and end_second are integer values representing the start and end of the subclip
## You may also uncomment the following line for a subclip of the first 5 seconds
##clip3 = VideoFileClip('test_videos/challenge.mp4').subclip(0,5)
clip3 = VideoFileClip('test_videos/challenge.mp4')
challenge_clip = clip3.fl_image(process_image)
challenge_clip.write_videofile(challenge_output, audio=False)



