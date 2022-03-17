import pandas as pd

#filename = "Compound"
#filename = "MakerDAO"
#filename = "Curve Finance"

#comments
#filename = "MakerDAO_comment"
filename = "Curve Finance_comment"

extension = filename + "_combined.csv"

df = pd.read_csv(extension)

print(df.describe())

#Remove duplicate titles
# df_dropdup = df.drop_duplicates(subset=['title'])

# print(df_dropdup.describe())

#Remove empty body
df_dropempty = df.dropna(subset=['body'])

print(df_dropempty.describe())

#remove [deleted]
df_dropdeleted = df_dropempty[df_dropempty['body'] != '[deleted]']
print(df_dropdeleted.count())

#remove [removed]
df_dropremoved = df_dropdeleted[df_dropdeleted['body'] != '[removed]']
print(df_dropremoved.count())

df_dropremoved.to_csv(filename + "_combined_cleaned.csv", index=False, header=True)
