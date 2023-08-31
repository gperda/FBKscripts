# Extract VOSTOK meaningful columns from ASCII point cloud x,y,z,nx,ny,nz, removing color columns
import pandas as pd
import sys

# Load the CSV file into a DataFrame

input = sys.argv[1]
output = input.replace('csv','xyz')
print('Importing file ', input)
df = pd.read_csv(input, sep =' ', float_precision='round_trip')

# Extract the x,y,z,nx,ny,nz columns
new_df = df.iloc[:, [0,1,2,6,7,8]]

# Save the extracted columns to a new CSV file
new_df.to_csv(output,sep=' ', index=False)

print('Script finished. Output written to ', output)