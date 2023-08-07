import Metashape
import csv

# Read input file containing photo id, gcp name, xImg (mm), yImg (mm)
def read_csv_file(filename):
    data = []
    with open(filename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data

def compute_pxcoords(chunk, gcp_file, output_file):
	print("Script started...")
	
	#Save active cameras information
	photos = []
	for camera in chunk.cameras:
		photos.append({
			"name": camera.label.replace('.tif',''),
			"sensorheight": camera.sensor.height,
			"sensorwidth":camera.sensor.width,
			"pxsize": camera.sensor.pixel_size
			})
				
	with open(output_file, 'w') as f:	# Open output file
		for marker in chunk.markers:
			if marker.reference.enabled:	#If the marker is selected in the reference pane
				for row in gcp_file:
					if (row['gcp'] == marker.label):
						for p in photos:
							cx = (camera.sensor.width-1)/ 2	#Coordinates of the center of the photo in px
							cy = (camera.sensor.height-1)/ 2
							if(row['photo_id'] == p['name']):
								xpx = cx + float(row['ximg'])/p['pxsize'][0]	#CRS conversion and translation
								ypx = cy - float(row['yimg'])/p['pxsize'][1]	# yImg and yPx axis are opposite, hence -
								print (marker.label + "," + row['photo_id'] + "," + str(xpx) + "," + str(ypx), file=f)
	print("Script finished")
	return 1

chunk = Metashape.app.document.chunk

#Input file path. Format: PHOTONAME (without '.tif'),GCPNAME,xIMG,yIMG
path_input = r"C:\Users\admin\Desktop\GRAZ\metashape\scripts\imgcoords_gcp.txt"

#Output file path. Format: GCPNAME,PHOTONAME,xPX,yPX
path_output = r"C:\Users\admin\Desktop\GRAZ\metashape\scripts\pxcoords_gcp.txt"
gcp_img_coords = read_csv_file(path_input)

compute_pxcoords(chunk, gcp_img_coords, path_output)