import Metashape

chunk = Metashape.app.document.chunk

with open(r"C:\Users\admin\Downloads\test\out.txt", "w") as f:
 print("MARKER,X,Y,Z", file=f)
 for m in chunk.markers:
  print("{},{},{},{}".format(m.label, m.position[0], m.position[1], m.position[2]), file=f)
  
f.close()