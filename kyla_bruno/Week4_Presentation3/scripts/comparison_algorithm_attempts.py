import cv2
import numpy as np
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt

# =======================
# 1. IMAGE PREPROCESSING 
# =======================
# GRAYSCALE ------------------------
# image1 = cv2.imread('Sheffield_Samples/has_multiple/h2114153_tissues/h2114153_melan_2.tif', 0) 
# image2 = cv2.imread('Sheffield_Samples/has_multiple/h2114153_tissues/h2114153_h&e_3.tif', 0)

""" 
# Check Results --------------
cv2.imshow('Image 1 Grayscale', image1)
cv2.imshow('Image 2 Grayscale', image2)

cv2.waitKey(0)
cv2.destroyAllWindows() 
"""

# REDUCE NOISE WITH BLUR -------------------------
# none seem to be making much of a difference
# Gaussian Blur
# blurred1 = cv2.GaussianBlur(image1, (5, 5), 0)
# blurred2 = cv2.GaussianBlur(image2, (5, 5), 0)

# Median Blur
# blurred1 = cv2.medianBlur(image1, 5)

# Bilateral Filter
# blurred2 = cv2.bilateralFilter(image2, 9, 75, 75)

""" 
# Check Results --------------
cv2.imshow('Image 1 Blurred', blurred1)
cv2.imshow('Image 2 Blurred', blurred2)

cv2.waitKey(0)
cv2.destroyAllWindows() 
"""

# ===========================
# 2. ACTUALLY FIND CONTOURS
# ===========================
# THRESHOLDING -----------------------------
# Fixed Threshold
#_, thresh1 = cv2.threshold(image1, thresh = 235, maxval=255, type=cv2.THRESH_BINARY) # above 235 becomes white
#_, thresh2 = cv2.threshold(image2, thresh = 255, maxval=255, type=cv2.THRESH_BINARY) 

# Otsu's Method
#_, thresh1 = cv2.threshold(image1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#_, thresh2 = cv2.threshold(image2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Adaptive Threshold
# thresh1 = cv2.adaptiveThreshold(image1, 150, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
# thresh2 = cv2.adaptiveThreshold(image2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# GET CONTOURS ----------------------
#contours1, _ = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#contours2, _ = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

""" 
Check Results ----------------
img1_copy = np.copy(image1)
img2_copy = np.copy(image2)

# draw contours
cv2.drawContours(img1_copy, contours1, -1, (0, 255, 0), thickness=10)
cv2.drawContours(img2_copy, contours2, -1, (0, 255, 0), thickness=10)

# display results
cv2.imshow('Contours on Image 1', img1_copy)
cv2.imshow('Contours on Image 2', img2_copy)
cv2.waitKey(0)
cv2.destroyAllWindows() 
"""

# =======================
# APPLYING THE ALGORITHM
# =======================
# Make images the same size ------
# workshopping to fix error with axes mismatch
""" 
def resize_image(img1, img2):
    h1, _ = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    
    # keep proportional
    if h1 != h2:
        img2_resized = cv2.resize(img2, (w2, h1))  
        return img1, img2_resized
    
    return img1, img2 
"""

# Refine the matching process ---------
# maybe add later on; dont want to mess iwth rn
# def icp(contour1, contour2):
#     neighbors = NearestNeighbors(n_neighbors=1).fit(contour2)
#     distances, _ = neighbors.kneighbors(contour1)

#     # (n_points, 2) format
#     contour1 = contour1.reshape(-1, 2)
#     contour2 = contour2.reshape(-1, 2)

#     # average distance between corresponding points
#     return distances.mean() 

""" 
# Check Results -------------- 
# need to get largest contours to run this; run in other file
distance = icp(contour1, contour2)
print(f"Matching distance: {distance}") 
"""

# Visualize Sample Image As Overlay ------------
# not meant to be run in this file; just seeing which functions to use
""" 
cv2.drawContours(image1, contours1, -1, (255, 0, 0), 2) 
cv2.drawContours(image2, contours2, -1, (0, 255, 0), 2)
cv2.imshow('Overlay', np.hstack([image1, image2])) 
"""
