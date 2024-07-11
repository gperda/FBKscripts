import Metashape
import numpy as np

chunk = Metashape.app.document.chunk

path = r"F:\eoptis\post_update_marker_coords.txt"

with open(path, "w") as f:
 print("Transformation matrix\n", np.array(chunk.transform.matrix), file=f)
 print("MARKER,X,Y,Z", file=f)
 for m in chunk.markers:
  t = chunk.transform.matrix.mulp(m.position)
  print("{},{},{},{}".format(m.label, t[0], t[1], t[2]), file=f)
  
f.close()