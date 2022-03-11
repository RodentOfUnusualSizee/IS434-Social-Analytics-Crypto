import os
import glob
import pandas as pd
os.chdir("/Users/brandon/Documents/GitHub/Reddit/datav2")

extension = 'MakerDAO'
all_filenames = [i for i in glob.glob('*.csv') if extension in i]

