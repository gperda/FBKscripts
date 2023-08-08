# Extract VOSTOK meaningful columns from ASCII point cloud x,y,z,nx,ny,nz, removing color columns

import pandas as pd

# Load the CSV file into a DataFrame
path = r"C:\Users\admin\Desktop\GRAZ\VOSTOK\graz_dense_medium_subsample.csv"
df = pd.read_csv(path, float_precision='round_trip')

# Extract the x,y,z,nx,ny,nz columns
new_df = df.iloc[:, [0,1,2,6,7,8]]

# Save the extracted columns to a new CSV file
new_df.to_csv(r'C:\Users\admin\Desktop\GRAZ\VOSTOK\vostok_input.xyz',sep=' ', index=False)