import Metashape, math
import numpy as np

def transform_coordinates(position, matrix):
	"""
	Applies the transformation matrix to the marker position.
	"""
	# Convert Metashape.Vector to a NumPy array (homogeneous coordinates)
	position_homogeneous = np.array([position.x, position.y, position.z, 1], dtype=np.float64)
	
	# Convert Metashape.Matrix to a NumPy array and reshape to 4x4
	matrix_np = np.array(matrix).reshape(4, 4)
	
	# Apply the transformation: matrix multiplication
	transformed_position_homogeneous = np.dot(matrix_np, position_homogeneous)
	
	# Convert back to Metashape.Vector (ignore the homogeneous coordinate)
	transformed_position = transformed_position_homogeneous[:3]
	
	return transformed_position

def vect(a, b):
	"""
	Normalized vector product for two vectors
	"""

	result = Metashape.Vector([a.y*b.z - a.z*b.y, a.z*b.x - a.x*b.z, a.x*b.y - a.y *b.x])
	return result.normalized()

def get_marker(label, chunk):
	"""
	Returns marker instance from chunk based on the label correspondence
	"""
	
	for marker in chunk.markers:
		if label == marker.label:
			return marker
	print("Marker not found! " + label)
	return False

chunk = Metashape.app.document.chunk
region = chunk.region

vertical = ["86.1000", "86.4000"]
horizontal = ["86.3000", "86.4000"]
vertical = get_marker(vertical[0], chunk).position - get_marker(vertical[1], chunk).position
horizontal = get_marker(horizontal[0], chunk).position - get_marker(horizontal[1], chunk).position


normal = vect(horizontal, vertical)
vertical = - vertical.normalized()
horizontal = vect(vertical, normal)

R = Metashape.Matrix ([-horizontal, -vertical, normal])
print(R.det())
region.rot = R.t()
chunk.region = region
R = chunk.region.rot		#Bounding box rotation matrix
C = Metashape.Vector([-1.4331003019372535,0.9416486798340593,-5.623293062800017])		#Bounding box center vector

if chunk.transform.matrix:
	T = chunk.transform.matrix
	s = math.sqrt(T[0,0] ** 2 + T[0,1] ** 2 + T[0,2] ** 2) 		#scaling # T.scale()
	S = Metashape.Matrix().Diag([s, s, s, 1]) #scale matrix
else:
	S = Metashape.Matrix().Diag([1, 1, 1, 1])
T = Metashape.Matrix( [[R[0,0], R[0,1], R[0,2], C[0]], [R[1,0], R[1,1], R[1,2], C[1]], [R[2,0], R[2,1], R[2,2], C[2]], [0, 0, 0, 1]])
chunk.transform.matrix = S * T.inv()		#resulting chunk transformation matrix		

# with open(r"F:\eoptis\transformed_coords.txt", "w") as file:
	# for marker in chunk.markers:
		# tc = transform_coordinates(marker.position, chunk.transform.matrix)
		# print("{},{},{},{}".format(marker.label, tc[0], tc[1], tc[2]) ,file=file)
		
		
with open(r"F:\eoptis\transformed_coords_new.txt", "w") as file:
	for marker in chunk.markers:
		tc = chunk.transform.matrix.mulp(marker.position)
		print("{},{},{},{}".format(marker.label, tc[0], tc[1], tc[2]) ,file=file)


print("Script finished")