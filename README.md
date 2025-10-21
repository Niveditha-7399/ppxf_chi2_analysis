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
