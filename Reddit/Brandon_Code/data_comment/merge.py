import os
import glob
import pandas as pd
os.chdir("/Users/brand/OneDrive/Documents/GitHub/IS434-Social-Analytics-Crypto/Reddit/data_comment")

#extension = 'MakerDAO_comment'
extension = 'Curve Finance_comment'
all_filenames = [i for i in glob.glob('*.csv') if extension in i]

combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])

combined_csv.to_csv(extension + "_combined.csv", index=False, header=True)

