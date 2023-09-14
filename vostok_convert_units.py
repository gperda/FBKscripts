import csv
import sys

# Convert meteo station solar radiation values from J/cm2 to Wh/m2

def read_csv_file(filename):
	data = []
	conv = 2.777778	#Conversion factor
	
	with open(filename, 'r') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			row['strahl'] = float(row['strahl']) * conv
			data.append(row)
		
	return data

def main():
	input_path = sys.argv[1]
	out = input_path.replace('.csv', 'whm2.csv')
	input = read_csv_file(input_path)
	
	with open(out, 'w') as f:
		print("date_and_time,solar_radiation[wh/m2]", file=f)
		for row in input:
			print (row['time'] + "," + str(round(row['strahl'],3)), file=f)
	
	print ("Conversion complete. See output file")
	
	return 1
	
main()