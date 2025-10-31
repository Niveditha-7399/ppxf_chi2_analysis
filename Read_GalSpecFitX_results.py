##############################################################
"""
This code is created by Niveditha Parthasarathy
and it is useful for reading the results
obtained using GalSpecFitX program

It takes in a folder (full of sub folders
containing the results for each observation) 
and reads the 'light_weights.png' file produced 
during the automated run and creates a single csv
file 'results_read_galspec.csv' in the results folder
with two columns- one has the names of the observations
and another with the ages retreived. It will 
write 'Not found' in case no age is retrieved
which can happen if the legend in the plot
covers the age value.

The compiled results csv will be created in the
input folder. I recommend checking this compiled csv
to find 'Not found' entries and manually update them.

"""
#################################################

#importing necessary packages 
import csv
import os
import re
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

#This should lead to your results folder that
#contains the sub-folders with results from GalSpecFitX
base_folder = r"C:\Users\nived\GalSpecFitX\nivis_results"

#Name of your compiled-results file that will
#created by this script
output_csv = 'results_read_galspec.csv'

#Regex pattern that can match variations of Age 
#and extract the number that comes after '<Age>'
age_pattern = r'(?:<|k|K)?Age[>\s:=]*([\d.]+)'

#Image will be processed here:
def preprocess_image(image_path):

    #setting it to grayscale and the edges are sharpened
    #contrast is increased and the image is 'enchanced'
    image = Image.open(image_path).convert('L')
    image = image.filter(ImageFilter.SHARPEN)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)    

    return image

#CSV compilation
with open(output_csv, mode='w', newline='') as file:

    writer = csv.writer(file)
    #here cluster name will be the folder name
    writer.writerow(['Cluster Name', 'Age'])

    #loop through each subfolder
    #open the plot with mean age in teh results sub folder
    for cluster_name in os.listdir(base_folder):
        cluster_path = os.path.join(base_folder, cluster_name)

        if os.path.isdir(cluster_path):
            image_path = os.path.join(cluster_path, 'light_weights.png')

            if os.path.exists(image_path):

                try:

                    #process the image and try to get the mean age text
                    image = preprocess_image(image_path)
                    custom_config = r'--oem 3 --psm 6'
                    text = pytesseract.image_to_string(image, config=custom_config)

                    print(f"OCR text from {cluster_name}:\n{text}\n")

                    #search for Age value and report to user if it is not found
                    match = re.search(age_pattern, text)
                    age_value = match.group(1) if match else 'Not found'

                    #write the retrieved result to CSV
                    #this will write 'Not found' in case
                    #no age is recognized
                    writer.writerow([cluster_name, age_value])

                #exception handling
                except Exception as e:
                    print(f"Error processing {cluster_name}: {e}")


