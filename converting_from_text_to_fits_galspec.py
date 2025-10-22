##############################################################
"""
This code is created by Niveditha Parthasarathy
and it is useful for preparing the observation spectra
for analysis in GalSpecFitX

It takes in text files and produces fits files

galspec needs the input to have a specific structure.
columns: wavelength, flux and error.
HDU is empty
HDU 1 can be empty with column structure
HD2 has the actual observation data

(you can change the config file segment
to adjust this, but I wanted to test with 
the sample provided in the software
and continued with this)
"""
#################################################

#importing necessary packages
import os
from astropy.table import Table
from astropy.io import fits
import numpy as np

#assigning path to the input and output
#the output folder will be created if not present
input_folder = r"C:\Users\nived\OneDrive\Desktop\RESEARCH\galspecfitx_nivi\obs\4_galspecfitx_obs_text_files_resampled_4200-5000_constant_error"
output_folder = r"C:\Users\nived\OneDrive\Desktop\RESEARCH\galspecfitx_nivi\obs\5_galspecfitx_obs_fits_files_resampled_4200-5000_constant_error_structure"
os.makedirs(output_folder, exist_ok=True)

print("\nStarting FITS creation for Galspecfitx, from TXT files to fits files with correct structure...")

#This will loop through all files in the input folder.
#If the files are not in TXT format then convert it to text before 
#running this program
#Also ensure that it has three columns- wavelength, flux and error

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        txt_path = os.path.join(input_folder, filename)

        try:
            data = np.loadtxt(txt_path)
        except Exception as e:
            print(f"Error loading {filename}: {e}. Skipping.")
            continue

        #Splitting the columns
        wavelength = data[:, 0]
        flux = data[:, 1]
        error = data[:, 2]

        # 1.Createing the Primary HDU0
        # This will be empty
        primary_hdu = fits.PrimaryHDU()

        # 2.Inserting a dummy data structure in HDU1
        dummy_table = Table(
            [np.array([]), np.array([], dtype=np.float32), np.array([], dtype=np.float32)],
            names=("wavelength", "flux", "error")
        )
        # EXTNAME matches galspec requirements
        hdu1_dummy = fits.BinTableHDU(dummy_table, name="ORIGINAL_SPECTRUM")

        # 3.HDU2 will have the observation data while
        #matching the required (D, D, D) format for galspecfitx.
        data_table = Table(
            [wavelength, flux, error],
            names=("wavelength", "flux", "error")
        )
        # again, extname matching galspec requirements
        hdu2_data = fits.BinTableHDU(data_table, name="RESAMPLED_SPECTRUM")

        # 4.Combining all the HDUs now
        hdul = fits.HDUList([primary_hdu, hdu1_dummy, hdu2_data])

        #The new fits files will have the same name as the text files
        output_filename = os.path.splitext(filename)[0] + ".fits"
        output_path = os.path.join(output_folder, output_filename)
        hdul.writeto(output_path, overwrite=True)

        print(f" Created FITS file: {output_filename}")

print("\nAll text files have been converted to FITS successfully with a compatible structure!")
