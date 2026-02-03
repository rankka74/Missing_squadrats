# 0,5k 1.4s python3 missing_squadrats.py squadrats-2026-02-01.kml Olli 24.859027260564833 60.220602974148186 24.947346246430854 60.197660629350736
# 5k 1.3s python3 missing_squadrats.py squadrats-2026-02-01.kml Olli 24.770523773101576 60.24742687505427 25.038256873130614 60.17788619144401
# 50k 2.5s python3 missing_squadrats.py squadrats-2026-02-01.kml Olli 24.52973612516265 60.310623797012106 25.341351115397025 60.099768666739884
# 350k 14s python3 missing_squadrats.py squadrats-2026-02-01.kml Olli 23.915899293552584 60.620612278297 26.103576753669447 60.02911120290123
# 1050k 14s python3 missing_squadrats.py squadrats-2026-02-01.kml Olli 23.18334864383624 60.89758612807452 26.992316334266196 59.869643254202145
# 2101k 14s python3 missing_squadrats.py squadrats-2026-02-01.kml Olli 22.392745132218305 61.10414236956497 27.779438898665266 59.6502656664513

import numpy as np
import time
import sys
import math
import os
import lxml.etree as ET
from shapely.geometry import Point, Polygon, LineString, MultiLineString, MultiPoint

# https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
  return (xtile, ytile)

# https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
# This returns the NW-corner of the square. Use the function with xtile+1 and/or ytile+1 to get the other corners. With xtile+0.5 & ytile+0.5 it will return the center of the tile.   
def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)

def readKmlFileTree(kmlFilePath):
  tree = ET.parse(kmlFilePath)
  data = ET.tostring(tree, encoding="unicode", pretty_print=True)
  # print ('Data: \r\n', data, '<BR>\r\n')
  data = data.split("<name>squadratinhos</name>")[1].split("<name>ubersquadrat</name>")[0].splitlines()
  return data

def readKmlFile(kmlFilePath):
  with open(kmlFilePath) as f:
    data = f.read()
    data = data.split("<name>squadratinhos</name>")[1].split("<name>ubersquadrat</name>")[0].splitlines()
  return data

def createGridLines(gridNW, gridSE, zoom):
  gridLines = []
  lines = []
  for x in range(gridNW[0], gridSE[0], 1): # lat, xtile, row, index 0, ~60
    for y in range(gridNW[1], gridSE[1], 1): # lon, ytile, col, index 1, ~25
      lat, lon = num2deg(x, y - 1, zoom)
      lines.append((lat, lon))
    gridLines.append(LineString(lines))
    lines = []
  print(x, y - 1, lat, lon, )
  lines = []
  for x in range(gridNW[1], gridSE[1], 1): # lon, ytile, col, index 1, ~25
    for y in range(gridNW[0], gridSE[0], 1): # lat, xtile, row, index 0, ~60
      lat, lon = num2deg(y, x - 1, zoom)
      lines.append((lat, lon))
    gridLines.append(LineString(lines))
    lines = []
  print(y, x - 1, lat, lon, )
  print(range(gridNW[0], gridSE[0], 1))
  print(range(gridNW[1], gridSE[1], 1))
  return gridLines

def createGridPoints(gridNW, gridSE, zoom):
  gridPoints = []
  for x in range(gridNW[0], gridSE[0], 1): # lat, xtile, row, index 0, ~60
    for y in range(gridNW[1], gridSE[1], 1): # lon, ytile, col, index 1, ~25
      lat, lon = num2deg(x + 0.5, y - 0.5, zoom)
      gridPoints.append((lat, lon))
  return gridPoints

def gridForLoop(nodeID, wayID):
  row = 0
  for rows in boundingBox: # lat
    col = 0
    for cols in rows: # lon
        # gridNW[0] = xtile = lat = row, gridNW[1] = ytile = lon = col
      pointCoordinates = num2deg(gridNW[0] + col + 0.5, gridNW[1] + row + 0.5, zoom)
      point = Point(pointCoordinates[0],pointCoordinates[1])
#    print(boundingBoxPolygon.contains(point))
      if boundingBoxPolygon.contains(point):
        boundingBox[row,col] = 1
        wayCoordinatesNW = num2deg(gridNW[0] + col, gridNW[1] + row, zoom)
        wayCoordinatesSE = num2deg(gridNW[0] + col + 1, gridNW[1] + row + 1, zoom)
        nodes.append((nodeID, wayCoordinatesNW[0], wayCoordinatesNW[1]))
        nodeID -= 1
        nodes.append((nodeID, wayCoordinatesSE[0], wayCoordinatesNW[1]))
        nodeID -= 1
        nodes.append((nodeID, wayCoordinatesSE[0], wayCoordinatesSE[1]))
        nodeID -= 1
        nodes.append((nodeID, wayCoordinatesNW[0], wayCoordinatesSE[1]))
        nodeID -= 1
        ways.append((wayID, nodeID + 4, nodeID + 3, nodeID + 2, nodeID + 1, nodeID + 4))
        wayID -= 1
#            print(nodeID)
#          print('Point: ', point, ', row: ', row, ', col: ', col)
      col += 1
    row += 1
  return nodes, ways

def points2lines(tilePoints, nodeID, wayID):
  for x in tilePoints.geoms:
    lat_deg = x.xy[0][0] # lat, xtile, row, index 0, ~60
    lon_deg = x.xy[1][0] # lon, ytile, col, index 1, ~25
#    print(lat_deg, lon_deg)
    xtile, ytile = deg2num(lat_deg, lon_deg, zoom)
    tileCoordinatesNW = num2deg(xtile, ytile, zoom)
    tileCoordinatesSE = num2deg(xtile + 1, ytile + 1, zoom)
    nodes.append((nodeID, tileCoordinatesNW[0], tileCoordinatesNW[1]))
    nodeID -= 1
    nodes.append((nodeID, tileCoordinatesSE[0], tileCoordinatesNW[1]))
    nodeID -= 1
    nodes.append((nodeID, tileCoordinatesSE[0], tileCoordinatesSE[1]))
    nodeID -= 1
    nodes.append((nodeID, tileCoordinatesNW[0], tileCoordinatesSE[1]))
    nodeID -= 1
    ways.append((wayID, nodeID + 4, nodeID + 3, nodeID + 2, nodeID + 1, nodeID + 4))
    wayID -= 1
  return nodes, ways, nodeID, wayID

def points2linesNoDuplicateNodes(tilePoints, nodeID, wayID):
  nodeID4 = nodeID
  for x in tilePoints.geoms:
    lat_deg = x.xy[0][0] # lat, xtile, row, index 0, ~60
    lon_deg = x.xy[1][0] # lon, ytile, col, index 1, ~25
#    print(lat_deg, lon_deg)
    xtile, ytile = deg2num(lat_deg, lon_deg, zoom)
    tileCoordinatesNW = num2deg(xtile, ytile, zoom)
    tileCoordinatesSE = num2deg(xtile + 1, ytile + 1, zoom)
    if (tileCoordinatesNW[0], tileCoordinatesNW[1]) in nodes:
#      print(nodes.index((tileCoordinatesNW[0], tileCoordinatesNW[1])))
      nodeID1 = nodeID - nodes.index((tileCoordinatesNW[0], tileCoordinatesNW[1]))
#      print(len(nodes))
    else:
      nodeID1 = nodeID - len(nodes)
      nodes.append((tileCoordinatesNW[0], tileCoordinatesNW[1]))
    if (tileCoordinatesSE[0], tileCoordinatesNW[1]) in nodes:
      nodeID2 = nodeID - nodes.index((tileCoordinatesSE[0], tileCoordinatesNW[1]))
    else:
      nodeID2 = nodeID - len(nodes)
      nodes.append((tileCoordinatesSE[0], tileCoordinatesNW[1]))
    if (tileCoordinatesSE[0], tileCoordinatesSE[1]) in nodes:
      nodeID3 = nodeID - nodes.index((tileCoordinatesSE[0], tileCoordinatesSE[1]))
    else:
      nodeID3 = nodeID - len(nodes)
      nodes.append((tileCoordinatesSE[0], tileCoordinatesSE[1]))
    if (tileCoordinatesNW[0], tileCoordinatesSE[1]) in nodes:
      nodeID4 = nodeID - nodes.index((tileCoordinatesNW[0], tileCoordinatesSE[1]))
    else:
      nodeID4 = nodeID - len(nodes)
      nodes.append((tileCoordinatesNW[0], tileCoordinatesSE[1]))
    ways.append((wayID, nodeID1, nodeID2, nodeID3, nodeID4, nodeID1))
    wayID -= 1
#  print(ways)
  return nodes, ways, nodeID, wayID

def shapely2osm(shapelyData, nodeID, wayID):
  with open("demofile.osm", "w") as f:
    f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    f.write("<osm version='0.6' upload='false' generator='JOSM'>\n")
    nodeIDCurr = nodeID
    for x in nodes:
      f.write("  <node id='" + str(x[0]) + "' lat='" + str(x[1]) + "' lon='" + str(x[2]) + "' />\n")
#      f.write("  <node id='" + str(nodeIDCurr) + "' lat='" + str(x[0]) + "' lon='" + str(x[1]) + "' />\n")
      nodeIDCurr -= 1
    for x in ways:
      f.write("  <way id='" + str(x[0]) + "'>\n")
      for y in x[1:]:
        f.write("    <nd ref='" + str(y) + "' />\n")
      f.write("    <tag k='highway' v='primary' />\n  </way>\n")
#      f.write("  <way id='" + str(x[0]) + "'>\n    <nd ref='" + str(x[1]) + "' />\n    <nd ref='" + str(x[2]) + "' />\n    <nd ref='" + str(x[3]) + "' />\n    <nd ref='" + str(x[4]) + "' />\n    <nd ref='" + str(x[1]) + "' />\n    <tag k='highway' v='primary' />\n  </way>\n")
    f.write("</osm>\n")
  return

def processGrid(data, gridPoints):
  crossing = 0
  data = data[0].split("<MultiGeometry>")[1].split("</MultiGeometry>")[0] # Crop the data
  polygonList = data.split("</Polygon><Polygon>") # Split data into polygons
  for x in polygonList:
    boundaryCoords = []
    interior = []
    exterior = []
    outerBoundaryIsList = x.split("<outerBoundaryIs>") # Split polygon into outer boundaries (exteriors)
    for y in outerBoundaryIsList[1:]:
      y = y.split("<coordinates>")[1].split("</coordinates>")[0] # Crop the outer boundary 
      wayLength = y.count(" ") + 1
      y = y.replace(" ",",").split(",")
# https://www.kubeblogs.com/how-to-process-kml-files-with-pythons-shapely-library-for-detecting-geo-boundaries/
      for z in range(wayLength): # Iterate the coordinates
        lat_deg = float(y[z*2+1])
        lon_deg = float(y[z*2])
        boundaryCoords.append((lat_deg, lon_deg))
        if SElat < lat_deg:
          if NWlat > lat_deg:
            if NWlon < lon_deg:
              if SElon > lon_deg:
                crossing = 1
    exterior = boundaryCoords
    innerBoundaryIsList = x.split("<innerBoundaryIs>")
    for y in innerBoundaryIsList[1:]:
      boundaryCoords = []
      y = y.split("<coordinates>")[1].split("</coordinates>")[0]
      wayLength = y.count(" ") + 1
      y = y.replace(" ",",").split(",")
      for z in range(wayLength):
        lat_deg = float(y[z*2+1])
        lon_deg = float(y[z*2])
        boundaryCoords.append((lat_deg, lon_deg))
        if SElat < lat_deg:
          if NWlat > lat_deg:
            if NWlon < lon_deg:
              if SElon > lon_deg:
                crossing = 1
      interior.append(boundaryCoords)
    if crossing == 1:
#      print(i, ' Time in the end of a polygon: ', time.perf_counter() - tic, ' seconds<BR>\r\n')
#      boundingBoxPolygon = boundingBoxPolygon - Polygon(exterior, holes = interior)
      gridPoints = gridPoints - Polygon(exterior, holes = interior)
      crossing = 0
  crossing = 0
  return gridPoints
  
def processGridTree(data, gridPoints):
  i = 0
  crossing = 0
  boundaryCoords = []
  for x in data:
    if "<LinearRing>" in x:
      print(data)
      x = data[i + 1]
      x = data[i + 1].split("<coordinates>")[1].split("</coordinates>")[0]
      wayLength = x.count(" ") + 1
      x = x.replace(" ",",").split(",")
# https://www.kubeblogs.com/how-to-process-kml-files-with-pythons-shapely-library-for-detecting-geo-boundaries/
      for y in range(wayLength):
        lat_deg = float(x[y*2+1])
        lon_deg = float(x[y*2])
        boundaryCoords.append((lat_deg, lon_deg))
        if SElat < lat_deg:
          if NWlat > lat_deg:
            if NWlon < lon_deg:
              if SElon > lon_deg:
                crossing = 1
      if "<Polygon>" in data[i - 2]:
        exterior = boundaryCoords
        interior = []
      else:
        interior.append(boundaryCoords)
#    print(i, crossing, data[i + 4])
      if crossing == 1 and "</Polygon>" in data[i + 4]:
#      print(i, ' Time in the end of a polygon: ', time.perf_counter() - tic, ' seconds<BR>\r\n')
#      boundingBoxPolygon = boundingBoxPolygon - Polygon(exterior, holes = interior)
        gridPoints = gridPoints - Polygon(exterior, holes = interior)
        boundaryCoords = []
        crossing = 0
      boundaryCoords = []
    i += 1
  return gridPoints

# Main program

zoom = 17
script_dir = os.path.dirname(__file__) + "/" #<-- absolute dir the script is in

tic = time.perf_counter()

# Sorting arguments
arguments = sys.argv
kmlFile = arguments[1]
userName = arguments[2]
NWlon = float(arguments[3]) # lon, ytile, col, index 1, ~25
NWlat = float(arguments[4]) # lat, xtile, row, index 0, ~60
SElon = float(arguments[5]) # lon, ytile, col, index 1, ~25
SElat = float(arguments[6]) # lat, xtile, row, index 0, ~60

# Calculate squadrats grid corners
gridNW = deg2num(NWlat, NWlon, zoom)
gridSE = deg2num(SElat, SElon, zoom)
print('Grid corners: ', gridNW, ' and ', gridSE, ', dimensions: ', gridSE[1] - gridNW[1], ' and ', gridSE[0] - gridNW[0])
# https://www.programiz.com/python-programming/matrix np.zeros( (rows, cols) )
boundingBox = np.zeros( (gridSE[1] - gridNW[1], gridSE[0] - gridNW[0]) )
boundingBoxPolygon = Polygon([[NWlat,NWlon], [NWlat,SElon], [SElat,SElon], [SElat,NWlon], [NWlat,NWlon]])
# print(boundingBox)

# Find the inner polygons that cross the bounding box
#	If none found, just make a grid for the whole bounding box
# Iterate all the points of the grid and check if they are inside of any of the selected inner polygons

missing_squadrats_dir = script_dir
kmlFilePath = missing_squadrats_dir + '/' + kmlFile
#kmlFilePath = kmlFile
print ('KML file: ', kmlFile, '<BR>\r\n')

# data = readKmlFileTree(kmlFilePath)
data = readKmlFile(kmlFilePath)

nodes = []
ways = []
boundaries = []
interior = []
nodeID = -4306537
wayID = -807654

print('Time after bounding box test: ', time.perf_counter() - tic, ' seconds<BR>\r\n')

gridPoints = MultiPoint(createGridPoints(gridNW, gridSE, zoom))

print('Time after grid creation: ', time.perf_counter() - tic, ' seconds<BR>\r\n')

#tilePoints = processGridTree(data, gridPoints)
tilePoints = processGrid(data, gridPoints)
# print(tilePoints)

points2lines(tilePoints, nodeID, wayID)

print('Time before osm write: ', time.perf_counter() - tic, ' seconds<BR>\r\n')

shapely2osm(tilePoints, nodeID, wayID)

print('Time after osm write: ', time.perf_counter() - tic, ' seconds<BR>\r\n')
print('Number of tiles: ', (gridSE[1] - gridNW[1]) *  (gridSE[0] - gridNW[0]))
#print('Time before osm write: ', time.perf_counter() - tic, ' seconds<BR>\r\n')


