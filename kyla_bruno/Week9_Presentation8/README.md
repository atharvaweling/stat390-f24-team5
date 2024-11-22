#data_science/stat390 
# Final Presentation
## Objectives (Priority Order)
1. Extract Tissue Slices - throw out blurry/unusable tissue samples during extraction. Automate process
	- OPTIONS: delete annotation before exporting, or delete unusable samples post exporting
2. Adaptive Pooling - improve adaptive pooling. why isnt it working on the 12x12s and how can we fix that. 
	- adding or tweaking conv layers? training on differnet image sizes? 
	- what should we consider for adaptive pooling since we want to scale things up? would scaling up and having three output classes influence the performance of adaptive pooling? the end goal is to have the same conv layers for all samples. then adaptive pool. then apply the same fully connected layers.

## Tissue Slice Extraction Improvements
1. Now able to work in any QuPath project. Can also make assumption that the user has already uploaded images into their QuPath project. 
	- The user only really needs the ``classifiers`` and ``scripts``
2. It's no longer necessary to change the image name format, as long as it has a stain name in it somewhere (will look for h&e, sox10, mela - case insensitive)
3. Program now automatically detects blurriness beyond a given threshold and deletes the image. 
	- currently using Python OpenCV. It is possible to do this in QuPath before exporting but it is not as effective. underestimates
4. No more manual merging, splitting, or deletion! Much faster and much less demanding (don't have to go through every individual annotation)
5. Program generalizes to new samples

