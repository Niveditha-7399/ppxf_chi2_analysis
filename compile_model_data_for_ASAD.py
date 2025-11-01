##############################################################
"""
This code is created by Niveditha Parthasarathy
and it is useful for preparing the model file
to analyze with Analyzer of integrated Spectra for Age,
henceforth abbreviated in thsi project as ASAD.

This script takes in a folder full of models in txt file format
and creates a single file out of it with the
first column being wavelength and the following
columns corresponding to flux1, flux2, flux3.. and so on.
where flux1 is the flux of the model file Indexed as 1,
similarly, flux2 is the flux of the model file Indexed as 2.


The indexing of model files is performed while keeping
track of the file names, and this indexing information
is also compiled in an output file.
"""
#################################################

#importing necessary packages
import os
import pandas as pd
from typing import Dict, List, Tuple

#################################################

#This is the setup for the program:

#This path should read to the folder full of
#models (in TXT format) that have to compiled into a single 
#text document
MODELS_FOLDER_PATH = r"C:\Users\nived\OneDrive\Desktop\RESEARCH\galspecfitx_nivi\asad\model\2_imf135_100_to_text"

#the name that you wish to give your new compiled-model file
COMPILED_FILE_NAME = 'novi_compiled_BPASS.txt'

#the name that you wish to give your index matching file
#this file will map the indeces in your model file
#to its information like age, metallicity etc
MAPPING_FILE_NAME = 'Output_info_BPASS.txt'

WAVELENGTH_COLUMN_NAME = 'Wavelength'

##################################################

#function definitions

def compile_model_data(models_path: str, compiled_output: str, mapping_output: str):
    """
    This function will read all the model files in the input folder at 
    MODELS_FOLDER_PATH, compile them into a single file. It also creates an
    index mapping file.

    """
    print(f"Starting the compilation of models from folder: {models_path}")
    
    #First we check if the models folder exists at models_path (MODELS_FOLDER_PATH)
    if not os.path.isdir(models_path):
        print(f"Error: Folder not found at {models_path}")
        return

    #This function will only take in TXT files
    all_files = [f for f in os.listdir(models_path) if f.endswith('.txt') and os.path.isfile(os.path.join(models_path, f))]
    if not all_files:
        print(f"No text files found in the folder: {models_path}")
        return

    #list to hold all DataFrames for merging
    #the mapping information (Index, File_Name) is also held in a list
    dataframes: List[pd.DataFrame] = []
    mapping_data: List[Dict[str, str or int]] = []
    
    #This will be the index counter for the flux columns
    flux_index = 1
    
    #Go through each file in the model folder after sorting 
    #this will ensure consistency
    for filename in sorted(all_files): 
        file_path = os.path.join(models_path, filename)
        
        try:
            #Reading the data 
            #Assuming the first column is Wavelength and the second is Flux
            #Using 'header=None' and 'sep' to take care of space/tab separation
            df = pd.read_csv(file_path, 
                              sep=r'\s+', 
                              header=None, 
                              names=[WAVELENGTH_COLUMN_NAME, f'Flux_{flux_index}'],
                              engine='python')
            
            #Join the DataFrame to the list, and the mapping information
            #to the corresponding variable
            dataframes.append(df)
            mapping_data.append({
                'Index': flux_index,
                'File_Name': filename
            })
            
            #This will be the flux index for the next file
            flux_index += 1
            
        #Exception handling
        except Exception as e:
            print(f"Skipping file '{filename}' due to error: {e}")

    #Compiling the data
    print("\nMerging data...")
    if not dataframes:
        print("No valid data to merge.")
        return

    #Starting with the first DataFrame
    compiled_df = dataframes[0]

    #Merge the following DataFrames one by one on the Wavelength column
    #'outer' join is safe to use in case 
    #of slight differences in wavelength grids
    #Assume all files share the same, consistent Wavelength grid- 'merge' works well.

    for i, df in enumerate(dataframes[1:], 1):
        compiled_df = pd.merge(compiled_df, df, on=WAVELENGTH_COLUMN_NAME, how='outer')
        
    print(f"Data merge complete. Total columns: {len(compiled_df.columns)}")

    #Formatting and saving the compiled file
    print(f"Saving compiled data to '{compiled_output}'...")

    #Header will have the list of flux column indices (1, 2, 3...)
    #with the columns being Wavelength, Flux_1, Flux_2, ...
    flux_column_indices = [str(i) for i in range(1, flux_index)]
    header_line = f"# {', '.join(flux_column_indices)}\n"

    #save the file
    with open(compiled_output, 'w') as f:
        f.write(header_line)
        
        #Writing the data, excluding the index and the column names 
        # (which will be the Wavelength column name)
        #and using space as the separator.
        compiled_df.to_csv(f, 
                           sep=' ', 
                           header=False, 
                           index=False,
                           float_format='%.8e')

    print(f"Successfully created compiled file: '{compiled_output}'")

    #the mapping file creation starts
    print(f"\nSaving mapping information to '{mapping_output}'...")
    
    #Create the mapping DataFrame and et the column order
    mapping_df = pd.DataFrame(mapping_data)
    mapping_df = mapping_df[['Index', 'File_Name']]
    
    #Saving the mapping file in a space-separated format
    mapping_df.to_csv(mapping_output, 
                      sep='\t', # Use tab for better column alignment
                      index=False) 

    print(f"Successfully created mapping file: '{mapping_output}'")
    
    return None


compile_model_data(MODELS_FOLDER_PATH, COMPILED_FILE_NAME, MAPPING_FILE_NAME)

print("\nProcess finished.")