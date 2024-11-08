# Presentation 6

#### Objective: 
- ***precisely*** answering padding related questions - Atharva and Parth 
- avoid manual intervention in tissue slice extraction
	- Team 3 requests steps 1-3 have the code refined to be easily executable by the stakeholders

## Instructions to Extract Tissue Slices

1. Download raw image data to your local directory if not already there. 
2. Run `1_rename_to_standard` to standardize the naming convention for all images
	- make sure to set directory to where you have put the raw image data
3. Open the QuPath project. Add the raw images
	- Delete mask images (will automate this next)
4. Automate --> Project Scripts --> master_script.groovy --> **Run for project** 
	- from here a user can review what will be exported (might be useful for stakeholder to review but if not, I will automate exporting as well)
	- when making GUI I'm thinking there can be a pause here where the user is prompted "Export Extracted Tissue Samples? Yes, No"
5. To export: Automate --> Project Scripts --> 6_export_annotations.groovy --> **Run**
	- 3 min 28 seconds to export 6 .tif files

>Note the difference between "Run for project" and "Run". The master script is meant to be run for the entire project while the export annotations script is built to simply "Run"

#### TLDR
- rename to standard
- load images to QuPath project. Delete masks
- master_script.groovy
- 6_export_annotations.groovy

## Next Steps
1. Automate skipping over or removing the mask images
	- check for QuPath setting to not create them in the first place

2. Make decisions for deletion process
	- detect images with abnormalities, then display to user and allow them to decide if sample should be used or not. User hits Yes/No to keep or not keep. Deletion/exclusion is then automated

3. Implement into GUI (make user friendly)
	- adjust code to take in input values from the user (eg. local directory where raw data is, yes/no selections, etc.) so the stakeholders don't have to directly work with code 
