# ppxf_chi2_analysis
This is a compilation of codes required for comparing two methods of full-spectrum fitting. For this analysis we use real spectral data from star clusters in the Megellanic clouds.

## galspecfitx_automate_run
This script is used for automating the process of analysing observations of star clusters using the ppxf spectral fitting software called GalSpecFitX. The repository was cloned from https://github.com/starivera/GalSpecFitX and in it an empty folder called 'nivis_results' was created along with a folder 'nivis_obs' which contains the fits files of observations.

To run the program, there should be a config file called nivi_config.ini that contains the necessary configuration settins for the observations. Note: The same configuration is used for all the observations. Only the file name changes in the config file (automatically).

This python file should be saved as 'galspecfitx_automate.py'

The program should be called as follows in the Anaconda prompt:
```
conda activate galspecfitx
cd galspecfitx
python galspecfitx_automate.py
```
## converting_from_text_to_fits_galspec
This script is used for the preparation of observation spectra for analysis with GalSpecFitX.
It takes in text files and produces fits files
galspec needs the input to have a specific structure: with columns being wavelength, flux and error.
HDU is empty
HDU 1 can be empty with column structure
HD2 has the actual observation data

(you can change the config file segment to adjust this, but I wanted to test with the sample provided in the software and continued with this)

## Read_GalSpecFitX_results
This code is created by Niveditha Parthasarathy and it is useful for reading the results obtained using GalSpecFitX program

It takes in a folder (full of sub folders containing the results for each observation) and reads the 'light_weights.png' file produced during the automated run and creates a single csv file 'results_read_galspec.csv' in the results folder with two columns- one has the names of the observations and another with the ages retreived. It will write 'Not found' in case no age is retrieved which can happen if the legend in the plot covers the age value.

The compiled results csv will be created in the input folder. I recommend checking this compiled csv to find 'Not found' entries and manually update them.

## compile_model_data_for_ASAD
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

## Attribution

This project includes helper code designed to work with [GalSpecFitX], which is licensed under the BSD 3-Clause License.

Original project:
- Author: Isabel Rivera
- Repository: [https://github.com/starivera/GalSpecFitX]



