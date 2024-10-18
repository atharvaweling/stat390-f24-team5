Kyla Bruno
#### Goal
work on identifying the same portion of a tissue across multiple stains, using Sheffield Rescan photos
1. For a given patient, develop an algorithm to identify the slices of different stains that are similar in structure, and can be used to take "matching samples" from the same region of the corresponding slice.
	- ***jump to step 5 for completion of this goal***
2. Once you have achieved one, develop an algorithm to take "matching samples" from the same region of the corresponding tissue slices

### Step 1: Make Pixel Classifiers
Used QuPath's "create thresholder" feature to create three pixel classifiers, one per stain type. These are stores in the `pixel_classifiers` folder. 
- ``find_tissue_h&e.json``
- ``find_tissue_melan.json``
- ``find_tissue_sox10.json``

Attempted to automate the process of applying the correct pixel classifier to each image so that annotations of the tissues in each image would generate automatically. However, I found that QuPath limitations prevent this and require manual loading of pixel classifiers. 

Then attempted to automate the process of annotating raw images by making separate scripts for each pixel classifier -- i.e. assuming the pixel classifier is already loaded, select just the images of the relevant stain type and apply to all. Could not get this to work either. It became less work to just annotate manually. 
- Plus side of this is that annotating manually allowed us to better discern which segments of tissue should be considered belonging to the same tissue. Some of the tissue samples are broken in pieces such that there are significant gaps between portions detected as tissue. All portions are detected as tissue, but are marked as different annotations (different tissues all together). To fix this, I manually grouped these cases into one annotation. 

### Step 2: Export Tissue Annotations
Wrote a script in the QuPath script editor to export annotations to my local directory in a designated directory format
- ``export_tissue.groovy`` - creates folder Tissues, then subfolders named using the raw image name. Each subfolder contains the tissue annotations found in that image, numbered as t1, t2, t3, etc. 
	- ``Stat_362/project/Tissues/h2114153_h&e.tif - Series 0/t_1.tif``
	- ``Stat_362/project/Tissues/h2114153_melan.tif - Series 0/t_1.tif``

To approach the next task, I decided to rearrange the individual tissue images to facilitate the task of identifying similar regions across stains. I wrote a python script that I ran in the terminal to edit my directory
- ``rearrange_samples.py`` - creates folder Sheffield_Samples, then creates subfolders for each unique image id (eg. ``h2114153_tissues``, ``h2114154_tissues``). This makes it clear that there are 13 unique images
	- Within each image folder are the individual tissue .tif files labelled with the unique image id, the stain type, and the tissue number within that image (eg. ``h2114153_h&e_t1.tif``, ``h2114153_melan_t1.tif``)
	- This format makes it clear how many, and which, tissues were extracted from each unique image and which have multiple stain types. For example, ``h2114158_tissues`` only has one tissue in sox10, while h2114156 has four tissues in h&e and two tissues in melan. 
- Both the ``Tissues`` and ``Sheffield_Samples`` folders were uploaded to the Team 5 shared Google Drive. 

***Note:** I completed steps 1 and 2 before I had access to Cara's method of exporting tissues. I can see that they were posted to the drive on Tuesday, but I worked on all of this over the weekend because for our team to start on our assignment we had to have the tissues exported. I have had my tissue classifier working since week 1 without any issues so I moved forward with it to have a baseline to work from for this week. I also wanted to organize the files in a way that made sense for my next steps/how i was thinking about this problem. *

### Step 3: Simple EDA
My first thought was to get a sense of the data we are working with. My group members are working on a version of this algorithm that matches similar tissue shapes no matter the stain (such that two h&e samples from the same patient may be paired). However, the wording in the given objective led me towards a slightly different approach, which focusses on finding corresponding samples across stains. 

In order to identify slices across stains, a given patient needs to have tissue samples in multiple stains. A quick look in the ``Sheffeild_Samples`` folder revealed that ***only 4 out of 13 patients have samples in more than one stain***.
- h21141*53*: 4 h&e, 2 melan
- h21141*56*: 3 h&e, 2 melan
- h21141*65*: 3 h&e, 1 sox10
- h21141*66*: 4 h&e, 1 sox 10

A quick look at the images shows that for each patient, every tissue sample looks pretty unique with the exception of patient 53
- melan_2 clearly matches h&e_4
- melan_1 appears to be the same as h&e_2, in a slightly different orientation

### Step 4: Make Plan for Algorithm
1. For a given patient, develop an algorithm to identify the slices of **different stains** that are similar in structure, and can be used to take "matching samples" from the same region of the corresponding slice.

**Initial Brainstorm** 
- Direct pixel wise comparison probs wont work well because of variation in stains, so instead I will focus on aligning ROIs based on shape/structure
- Pull outline of shapes, layer over one another, get percentage of overlap
- Iterative Closest Point method (mentioned by TA)

#### Final Outline
##### 1. Image Processing 
- To make shape/contour detection easier
	- convert to grayscale?
	- reduce noise (Gaussian blur)
##### 2. Actually Find Contours
- thresholding to separate tissue from background (may not be necessary)
	-  `cv2.threshold()` or `cv2.adaptiveThreshold()` 
- AND/OR contour detection to get tissue boundaries
	- ``cv2.findContours()``
##### 3. Contour matching across stains
- Use a shape similarity metric
	- eg. `cv2.matchShapes()` 
- Align contours better with ICP
	- `sklearn.neighbors` may have tools for this; look into
##### 4. Quantify Overlap
-  intersection and union tools?
- Set a percentage that determines if overlap is significant (high similarity)
- might be helpful to make a visual that layers the contours on top of one another so that we can see the overlap ( `cv2.drawContours()`may work)

##### Considerations for Improving/Developing the Algorithm
- **Normalizing Orientation** - make sure all images have a similar orientation. 
	- Since all the images were processed the same in QuPath, it appears they already have the same orientation, so I will add this to the algorithm later on if I think it may improve results to make minor adjustments to orientation
	- OpenCV's `cv2.getRotationMatrix2D()` and `cv2.warpAffine()`
- **Scaling** - Don't want images to be drastically different sizes, but again I don't think this is an issue we will run into. Will add later on if it appears necessary. 
	- `cv2.resize()` for rescaling.
- **Matching key points** - could add to make the shape comparisons better, but for now I am trying to get a baseline algorithm to work
	- look into SIFT or SURF or other feature-based methods for this
   
### Step 5: Write Scripts to Implement Algorithm
``comparison_algorithm_functions.py`` contains the final versions of three functions used to implement this algorithm as well as the code used to test each of the functions on sample images
- ``threshold_tissue()`` - takes in an image, converts to gray scale, and handles noise by identifying and removing small contours; shows the binary image created by the threshold
- ``extract_tissue_contour()`` - creates a copy of the image to draw the contours on; doesn't necessarily need to be it's own function, but was easier to separate out for testing
- ``compare_contours()`` - outputs the similarity score of the 2 input images along with each image with its contour drawn on 
- Function to visualize overlay (in development)

``comparison_algorithm.py`` - successfully runs the algorithm on all of the patient folders that have multiple stains and outputs tissue samples with a similarity score above 95
-  I had originally planned to write the algorithm all in one script, but Parth took the approach of separating out/defining functions. Since we plan to run this algorithm on a whole batch of images, I decided to mimic this by creating a script to hold helper functions, and a script that will actually apply the functions to the entire data set. (credits to Parth)
- right now is comparing every image to every image regardless of stain, but can change to only compare across stains!
- can also adjust threshold for inclusions as similar
	- remember to press any key to progress from one image to the next!!
 
``algorithm_attempt1.py`` was used as a playground for a variety of techniques I tried out for this algorithm. It is where I started and decided which methods to implement in the actual functions.
- I included this as a documentation of progress and attempted implementations. It also contains preliminary attempts at functions I plan on implementing (one to resize images if needed, and one to display contoured images as an overlap with one another)
- not meant to be run

#### Some Things to Debug
- it appears that one sample has a horizontal orientation that can be fixed by rotating it
- right now the rotation through the pairs is repeating pairs s.t. (imageA, imageB) is considered different than (imageB, imageA)
