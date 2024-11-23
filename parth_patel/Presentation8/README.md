****Multistain Image Classification****

*Purpose:* <br>
Multichannel CNN used on small sample dataset of patches. 3 channels for each 3 stains, leading to 3x3 = 9 total channels for combined patch.
<br>

*Steps:*
1. Run the pipeline code to make patches across stains
2. Selected few patient level patches (meaning a patch folder with all 3 stains) and moved to folder patches_selected (done because patching is not perfect)
3. Open severity_labels.py and add severity label to patient_severity dictionary. Run creating severity_labels.csv
4. Open mod_con.py and adjust patches_dir to directory leading to the patches_selected folder. The folder is shown below.
5. Results should be generated.

<img width="777" alt="Screenshot 2024-11-22 at 5 36 11 PM" src="https://github.com/user-attachments/assets/24f64005-597c-4ea8-851a-262f67d6c740">

<br>
<br>
My patches_selected folder can be accessed through drive: <br>

[patches_selected_folder](https://drive.google.com/drive/folders/1B78v-09RlqeZTSoDwpmn2t6K_YiWSYlr?usp=drive_link)
