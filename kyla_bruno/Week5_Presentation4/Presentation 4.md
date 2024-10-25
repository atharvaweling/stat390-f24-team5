# Presentation 4

Summary of all presentation 3s (18th Oct): [spreadsheetLinks to an external site.](https://docs.google.com/spreadsheets/d/1khao3unpj_vsx4kOSg_Zzo77YK1UWL2w73Oa0aAirOo/edit?usp=sharing)
Submissions of all teams are uploaded on [OneDriveLinks to an external site.](https://nuwildcat-my.sharepoint.com/:f:/g/personal/akl0407_ads_northwestern_edu/Eu2kf1KKjZxGuP0Ca-u3MG4B1Wv3dtcLshEfhrxPKA72nA?e=v5Gbqf). 
#### Objective
1. Test out Noah's algorithm rigorously, identify cases where it fails, and then think of ideas to fix it
	- Team 1 has tried a comprehensive set of methods _(check the spreadsheet)_ that may be used to fix any potential failures of Noah's algorithm. 
	- Don't use ORB or histogram methods
2. If it seems to have no issues, move to the next objective of sampling from the matching slices! 
### tldr
Updates to the notebook have focussed on handling errors that arise from variability in the amount, directory location, and naming of patches. Other changes focussed on making the user experience more adaptable and robust, particularly by handling errors that would otherwise stop the program or cause inaccurate output. 

### Step 1: Get Noah's Code Working Locally
I first downloaded Noah's code from OneDrive and explored each file to get a better understanding of his work. I tested out the code using the samples he had in the ``/patients`` directory to test that the scripts were running as intended. 
- It took me a bit to go through the ``gui.py`` and ``separate.py`` scripts and parse out what each line was doing (I'm from the R track and have no experience with making a GUI in Python)

I did not use Noah's ``separate.py`` script to extract and export individual tissues to my local directory because I did this in my local directory last week. I simply copied over the tissue samples from the three patients above into my new workspace. 

After determining that I did not need to use the ``gui.py`` and ``separate.py`` scripts I deleted them from my directory. However, I did find going through them very informative and helpful to my learning process in the notebook later on. 
- It also got me thinking about setting up ways for a user to run the code we implement easily (GUI for the stakeholders)

### Step 2: Identify Testing Samples
To test out Noah's algorithm, I collected tissue samples from patients that Noah did not use as examples and stored them in a folder called `/test_samples`. The patients were
- h21141***56*** - 3 h&e, 2 melan
- h21141***65*** - 3 h&e, 1 sox 10
- h21141***66*** - 4 h&e, 1 sox 10
- h21141***58***- only one sox10
- h21141***90*** - 4 tissue samples, all in same stain (h&e)

### Step 3: Fixing Bugs 
##### Bug 1: Handle NotADirectory Error
The `read()` function kept throwing an error on my local machine because it was getting caught on the hidden system `.DS_Store` file that macOS automatically creates in directories. Since we do not know the operating system or specific contents of a potential user's directory, it is important we handle this case. 
- the `read` function now handles any non-directory files that may be present (or hidden) in a user's given directory
##### Bug 2: Handle All File Types
I first was getting an error because the original version of the `read()` function could only handle .jpg files. I made minor changes to the ``read()`` function to handle .tif files, but then decided to catch cases for all file types. 
- function now uses ``Image.Open()`` function from the Pillow library to handle a wider range of file types
- function will not throw an error if the user were to input an unsupported file type; displays a warning message "This is not a supported file type"
##### Bug 3: Handle KeyError
Next, the `show()` function threw an error because of the absence of a sox10 folder in the given patient's directory. I don't have a sox10 folder in the directory for patient h2114156 simply because they have no tissue samples in the sox10 stain.

It's an inefficient use of resources to initialize empty folders and search through them, especially if we scale up the use of these functions. I also hope that we would be able to provide the user with some flexibility in the construction of their machine's directory. 

For these reasons, I expanded the `read()` function to handle cases where a particular patient doesn't have samples in all three stains. From the data I've looked at, it seems that most of the patients fall into this category. 
- I started by attempting to handle this within the `show()` function, but it required manually searching for missing stains so I added to the `read()` function instead

The updated version of the `read()` function can now handle instances where a patient has tissues in only some of the stains, removing the need to initialize an empty folder for each stain type. It also now displays a warning message to the user when a particular stain is not found for a patient, making it easy to know that the stain has been considered but is absent. 

### Step 4: Test Edge Cases
My group members were working more on the algorithm itself and its accuracy in computing similarity, so I went in the direction of considering the variety in patient portfolios -- ie. the type and amount of samples they have in a given folder. The goal here is to increase the flexibility of the program for users (clears a lot of roadblocks for stakeholders). 

##### Case 1: All samples are in the same stain
Our particular use-case does not require comparison between tissues of the same stain. The original `read()` function did not consider this, unnecessarily loading in images. Theoretically this could (and maybe should) be implemented when tissue samples are exported. I did this in Week4_presentation3 by separating patients with only one stain type from patients with multiple stains. However, I figure this directory setup is not universal. 
- it will be useful to automate separating patients that need tissue comparison (have multiple stains) and those that don't (stains of only one type)

##### Case 2: Patient only has one tissue sample
When a patient has only one tissue sample, the axes variable used in the `show()` function is not a list, resulting in an error if not addressed directly. Fixing it allows for flexibility in input such that the user does not need to know the contents of each patient's folder beforehand. 

### Step 5: Update Existing Functions
`extract_main_contour()`: updated to handle PIL images by converting them to a NumPy array

``similarity_matrix(set1, set2, names)``: updated to include axis labels

`pipeline()`: 
- now can handle images passed in as a dictionary instead of an array 

`read()`: allows for more flexibility in a user's directory and handles errors without stopping functionality (eg. can have one invalid image in an entire directory and the program won't stop)
- handles non-directory files
- handles broader range of image types
- handles invalid image types 

##### Other Changes
- standardized strings to lowercase for the read and show functions to handle naming inconsistencies
- rather than stop when a stain is not found, it will continue to check for the presence of samples in the other requested stains. 
- uses a grid to display samples - more adaptable to space available and size/number of image
- now has a feature that lists all the possible sample combinations across stains that can be made for a given patient.


### Step 6: Add New Functions
``print_similarity_scores(similarity_matrix, set1, set2, names)``: was more for debugging when I noticed that similarity scores were not properly being extracted and sorted from the similarity matrix 
- stores the indices of similarity scores to make them easily accessible. 

``display_similar_combinations(matching_indices, set1, set2, names)``: improves user experience by not only showing a similarity matrix, but by displaying samples found to be similar side by side for manual viewing. 
- makes it much easier to check and visualize results
- all the information a user needs can be provided based on their specifications; basis for an expanded GUI
