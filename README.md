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
