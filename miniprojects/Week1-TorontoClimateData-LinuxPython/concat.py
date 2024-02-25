#!/usr/bin/python3

import os
import glob
import pandas as pd
os.chdir("~/toronto_climate_data/inputfiles")

filenames = [i for i in glob.glob(f'*.csv')]

concat_files = pd.concat([pd.read_csv(i) for i in filenames ])
os.chdir("~/toronto_climate_data/outputfiles")
concat_files.to_csv( "all_years.csv")