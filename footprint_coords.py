#compatibility Metashape Pro 2.0.2
#Creates footprint shape layer in the active chunk for each camera, post alignment

import Metashape

doc = Metashape.app.document
chunk = doc.chunk

if not chunk.shapes:
	chunk.shapes = Metashape.Shapes()
	chunk.shapes.crs = chunk.crs
T = chunk.transform.matrix
footprints = chunk.shapes.addGroup()
footprints.label = "Footprints"
footprints.color = (30, 239, 30)

if chunk.point_cloud:
	surface = chunk.point_cloud
elif chunk.model:
	surface = chunk.model
else:
	surface = chunk.tie_points
	
for camera in chunk.cameras:
	if not camera.transform:
		continue #skipping NA cameras
	
	sensor = camera.sensor
	corners = list()
	for i in [[0, 0], [sensor.width - 1, 0], [sensor.width - 1, sensor.height - 1], [0, sensor.height - 1]]:
		corners.append(surface.pickPoint(camera.center, camera.transform.mulp(sensor.calibration.unproject(Metashape.Vector(i)))))
		if not corners[-1]:
			corners[-1] = chunk.point_cloud.pickPoint(camera.center, camera.transform.mulp(sensor.calibration.unproject(Metashape.Vector(i))))
		if not corners[-1]:
			break
		corners[-1] = chunk.crs.project(T.mulp(corners[-1]))
		
	if not all(corners):
		print("Skipping camera " + camera.label)
		continue
		
	if len(corners) == 4:
		shape = chunk.shapes.addShape()
		shape.label = camera.label
		shape.attributes["Photo"] = camera.label
		shape.group = footprints
		shape.geometry.type = Metashape.Geometry.Type.PolygonType
		shape.boundary_type = Metashape.Shape.BoundaryType.OuterBoundary
		shape.geometry = Metashape.Geometry.Polygon([Metashape.Vector([coord.x, coord.y]) for coord in corners])

		
Metashape.app.update()
print("Script finished")