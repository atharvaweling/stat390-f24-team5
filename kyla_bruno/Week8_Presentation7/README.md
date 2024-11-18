# Presentation 7 Summary

##### (1) Corrected code so that it executes on anyone's system. Shared to GitHub
- Updated directory paths to be general. Will get the location of the `Extracted_Tissues` folder in a user's directory and navigate to the pixel classifiers from there
- Removed the giant debris in the sox10s with a max area restriction and thresholder settings
- Inserted try/catch statements to handle errors in a more user friendly/informative way
- Cleaned up names when exporting
- Cleaned up console output when exporting so user can see the progress (where the program is in their folder of images)
- Improved structure/looping to decrease complexity
- Handled automatic generation and removal of image masks - no longer needs manual removal!
- Generated tissue slice .tif files for all Sheffeild Sox10s
- All of the manual intervention required by the user necessary for Cara's extraction process has been automated
- if a user wants to work from their own project, only need to download `classifiers` and `script` folders and put them in project directory

##### Next Steps
- Talk with GUI team about formatting to fit into their design (unsure how to do this without their plan):
	- option to prompt the user to delete ambiguous samples (eg. h&e_h2125906 t_3)
	- option to prompt the user to export and choose a location to export to
	- position directory organizing/renaming scripts (eg. `rename_to_standard`) at a sensible place within the workflow
- Finish extracting tissue slices for the remaining samples/new samples. Continue to debug if needed
	- I've been trying to break it because I figure better to handle edge cases/debugging sooner rather than later. I want to make sure it holds up in a wide range of scenarios
	- I'd like to do some more debugging on the edge cases and compare the results with Cara's to see what's coming up the same/different. Adjust thresholder if needed.
- Run program on a different operating system. I used MacOS and want to ensure that nothing comes up when run on a different OS (eg. like when Noah's code worked on Linux but not Mac bc of "hidden source files")
- Make sure QuPath 0.5.1 isn't going anywhere and if it is, how we can handle that
	- As I've been writing QuPath scripts, it seems there are a lot of changes from version to version, especially in function names and method availability
	- QuPath's newest version (6) is set to release very soon and may have unexpected differences (according to QuPath discussion boards)

---
##### (2) Watched the CNN image classification video posted in the announcement. 
- Found the model output when adaptive pooling is applied. Used "patterns" sheet examples
	- trained on cases 1 and 2
	- assessed performance on cases 3 and 4
- Learned how to implement a simple Neural Network using PyTorch
- Learned how to implement a Convolutional Neural Network using PyTorch
	- used a predefined filter in the first convolutional layer to match the video and practice this kind of implementation. 
		- using the predefined 3x3 filter also helps prevent overfitting to the extremely small training set
		- this also makes it easier to apply the filters referenced in the patterns sheet if that is what those are intended for?
- Read about adaptive pooling, the mechanisms behind it, and best use cases
	- *adaptive pooling and proportional pooling are two different things*
- Constructed an Adaptive Pooling CNN using PyTorch that can handle shifted images, padded images, rectangular images, and larger patterned squares. 
	- two convolutional layers
	- added one adaptive pooling step - a different pooling window is applied depending on the image size
	- only one hidden layer
	- made sure to get expected 4D output 
- Found the Adaptive Pooling CNN Model score for Case 4 (and case 3) examples. Generated confusion matrices
	- model f1 score: 0.80
	- model accuracy score: 0.667
		- 12x12 image: actual = 0, predicted = 1
		- 18x18 image: actual = 0, predicted = 0
		- 24x24 image: actual = 0, predicted = 0
- Analyzed how different-sized images with adaptive pooling effect the model score and classification (see [[#Results/Discussion]])

---
### Results/Discussion

The adaptive pooling CNN model achieves **100% accuracy** and an **F1 score of 1.00** on the training data (case 1 and 2), which makes sense considering only 4 samples, all 6x6, were used.  

On Case 4's larger images (12x12, 18x18, 24x24), the accuracy drops to **66.67%**, and the **F1 score decreases to 0.80**. This is a fairly large jump numerically, but really only indicates that the model classified one image incorrectly, the 12x12. The confusion matrix (see notebook output) informs us that the model's misclassification mistook what was actually an "O" for an "X". We see the model also mistook an "O" for an "X" on the 12x12 padded image from Case 3. This is the only example from Case 3 that the model classified incorrectly. 

The misclassification of an intermediate sized image, but not larger or unevenly sized ones, is interesting. The adaptive pooling layer compresses all inputs to a fixed 4x4 output, which may work better for some image sizes than others. For example, the pooling may disproportionately emphasize features near the edges in 12x12 images, but evenly (and effectively) distribute features across pooling regions for the larger images. See intermediate results in notebook output. 

This could also be explained by training the model exclusively on 6x6 images, as the model would likely perform better with more than 4 training examples to work from. As it stands, the model may be overfitting smaller scale patterns, getting confused by the intermediate size of the 12x12. In other words, the model may lack the exposure to intermediate-sized training patterns that allow it to generalize well to this specific size. 

Furthermore, it doesn't seem like adaptive pooling is made to address the repeated patterns we see in Case 4 -- ie. patterns in images of different sizes and/or the same pattern viewed by zooming in or out. For this reason, I was surprised to see how well the model did on the repeated pattern images, although this could change depending on the output goal, which in this case was to only detect the presence of at least one "O" or "X". 

Overall, the adaptive pooling model performs well with varied input sizes, but the imperfect results indicate that the model requires more fine-tuning or even enhanced preprocessing. 
##### To Improve the Model
- Augment training data to include larger and more diverse image sizes
- Experiment with more convolutional layers or global pooling to capture more robust patterns before adaptive pooling.
- Play around with parameters and fixed output size
- Fine-tune the loss function (or perhaps add regularization) 
