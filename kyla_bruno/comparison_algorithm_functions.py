import cv2
import numpy as np

# =======================
# 1. IMAGE PROCESSING 
# =======================
def threshold_tissue(image, white_threshold = 220): # almost white; can change if needed
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # fixed thresholding is workign best here
    _, tissue_masked = cv2.threshold(image, white_threshold, 255, cv2.THRESH_BINARY_INV)

    # smooth out to remove noise
    kernel = np.ones((3, 3), np.uint8)
    tissue_mask = cv2.morphologyEx(tissue_masked, cv2.MORPH_OPEN, kernel)

    # get the contours
    contours, _ = cv2.findContours(tissue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # dont want super small contours
    for contour in contours:
        area = cv2.contourArea(contour)
        # can change this area
        # currently filling in small contours with black, but can change if want to id these
        if area < 800:
            cv2.drawContours(tissue_mask, [contour], -1, (0, 0, 0), -1)

    return tissue_mask, contours

'''
# TESTING
image = cv2.imread('Sheffield_Samples/has_multiple/h2114153_tissues/h2114153_h&e_3.tif')
tissue_mask = threshold_tissue(image, 220)

cv2.imshow('Tissue Mask', tissue_mask)
cv2.waitKey(0)
'''

# ===========================
# 2. ACTUALLY FIND CONTOURS
# ===========================
# save space calling both functions by putting threshold in this one w same args
def extract_tissue_contour(image, white_threshold=220):
    _, contours = threshold_tissue(image, white_threshold)

    # draw contours on a copy for viewing
    contoured_image = image.copy()
    cv2.drawContours(contoured_image, contours, -1, (0, 255, 0), 10)

    return contoured_image, contours

'''
# TESTING
image = cv2.imread('Sheffield_Samples/has_multiple/h2114153_tissues/h2114153_h&e_3.tif')
final_image, contours = extract_tissue_contour(image, 220)

cv2.imshow('Tissue W/ Contour', final_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''

# ==================================
# 3. Contour Matching Across Stains
# ==================================
# might not need this white_threshold argument in any of these if 
# it works well on all images set at 220
def compare_contours(image_1, image_2, white_threshold=220):
    # get contours
    _, contours_1 = extract_tissue_contour(image_1, white_threshold)
    _, contours_2 = extract_tissue_contour(image_2, white_threshold)

    # catch if there are no contours found for some reason
    if len(contours_1) == 0 or len(contours_2) == 0:
        return float('inf') 

    # going to use largest contour just in case
    # i already remove small areas, but this will select only 1 for comparison
    # just in case there are multiple large pieces that pass area-wise (eg. h53 melan_2)
    contour_1 = max(contours_1, key=cv2.contourArea)
    contour_2 = max(contours_2, key=cv2.contourArea)

    # get similarity from comparison
    similarity_score = cv2.matchShapes(contour_1, contour_2, cv2.CONTOURS_MATCH_I1, 0.0)

    return similarity_score

'''
# TESTING
image1 = cv2.imread('Sheffield_Samples/has_multiple/h2114153_tissues/h2114153_h&e_3.tif')
image2 = cv2.imread('Sheffield_Samples/has_multiple/h2114153_tissues/h2114153_melan_2.tif')

similarity = compare_contours(image1, image2, white_threshold=220)

print(f"Similarity Score: {similarity}")

# display to review results
# can maybe write a function to do this for when you run on whole folder
image1, _ = extract_tissue_contour(image1, 220)
image2, _ = extract_tissue_contour(image2, 220)

cv2.imshow('Image 1', image1)
cv2.imshow('Image 2', image2)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''

# Next steps: Function to Visualize Overlay 
