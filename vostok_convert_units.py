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
	path = r'C:\Users\admin\Desktop\GRAZ\VOSTOK\klima-daily_20220101T0000_20230101T0000.csv'
	out = path.replace('.csv', 'whm2.csv')
	input = read_csv_file(path)
	
	with open(out, 'w') as f:
		print("time,station,solar_radiation", file=f)
		for row in input:
			print (row['time'] + "," + row['station'] + "," + str(round(row['strahl'],3)), file=f)
	return 1
	
main()