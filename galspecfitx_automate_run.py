
"""
Created by Niveditha Parthasarathy

This script is used for automating the process of 
analysing observations of star clusters using
the ppxf spectral fitting software called GalSpecFitX
    
The repository was cloned from 
https://github.com/starivera/GalSpecFitX
and in it an empty folder called 'nivis_results' was created
along with a folder 'nivis_obs' which contains the fits files
of observations.

There should be a config file called nivi_config.ini
that contains the necessary configuration settins for 
the observations.

Note: The same configuration is used for all the observations.
Only the file name changes in teh config file (automatically).
    
This python file should be saved as 'galspecfitx_automate.py'

The program should be called as follows in the Anaconda prompt:
'
conda activate galspecfitx
cd galspecfitx
python galspecfitx_automate.py
'
"""

###############################################################
#Importing necessary packages and performing initial setup
###############################################################
import os
import shutil
import subprocess

BASE_PATH = r"C:\Users\nived\GalSpecFitX"
OBS_FOLDER = os.path.join(BASE_PATH, "nivis_obs") 
CONFIG_TEMPLATE = os.path.join(BASE_PATH, "nivi_config.ini")
RESULTS_BASE = os.path.join(BASE_PATH, "nivis_results")

#This will create the results file if it is not present 
os.makedirs(RESULTS_BASE, exist_ok=True)

###############################################################
#THE AUTOMATION PROGRAM
###############################################################
for filename in os.listdir(OBS_FOLDER):
    #only reads the text or fits files (spectra)
    if not filename.lower().endswith((".txt", ".fits")):
        continue  

    #for each spectrum, a folder is created in the 
    #results folder that with the name of the
    #spectrum.

    #file_path = os.path.join(OBS_FOLDER, filename)
    run_name = os.path.splitext(filename)[0]
    run_folder = os.path.join(RESULTS_BASE, run_name)
    os.makedirs(run_folder, exist_ok=True)

    #A copy of the config file is created for each spectrum
    new_config_path = os.path.join(run_folder, f"{run_name}_config.ini")
    shutil.copy(CONFIG_TEMPLATE, new_config_path)

    #The data from the config file is parsed and
    #the line with the spectrum name is found and
    #changed to the current spectrum in the loop
    with open(new_config_path, "r") as f:
        lines = f.readlines()

    with open(new_config_path, "w") as f:
        for line in lines:
            if line.strip().startswith("galaxy_filename"):
                f.write(f"galaxy_filename = {filename}\n")
            else:
                f.write(line)

    #lets us know in the command line on which spectrum is
    #currently analyzed and then passes the necessary
    #arguments to the program
    print(f"\nRunning GalSpecFitX for {filename} ...")
    command = [
        "galspecfitx",
        "--config_file", new_config_path,
        "--output_path", run_folder
    ]

    #Task completion notification along with Error handling
    try:
        subprocess.run(command, check=True)
        print(f" Completed: {run_name}")
    except subprocess.CalledProcessError as e:
        print(f" Error during {run_name}: {e}")
        return None