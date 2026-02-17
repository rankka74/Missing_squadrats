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
import shutil
import datetime
from pathlib import Path
import subprocess

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

def createGridPoints(gridNW, gridSE, zoom):
  gridPoints = []
  for x in range(gridNW[0], gridSE[0], 1): # lat, xtile, row, index 0, ~60
    for y in range(gridNW[1], gridSE[1], 1): # lon, ytile, col, index 1, ~25
      lat, lon = num2deg(x + 0.5, y - 0.5, zoom)
      gridPoints.append((lat, lon))
  return gridPoints

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
  nodes.sort(reverse=False)
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
  with open("newsquadrats.osm", "w") as f:
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
      gridPoints = gridPoints - Polygon(exterior, holes = interior)
      crossing = 0
  crossing = 0
  return gridPoints

def osm2img():
  # Create output dir
  dateNow = datetime.datetime.now()
  dir = dateNow.strftime("%Y%m%d")
  abs_dir_path = Path(__file__).parent.parent.parent / dir
  try: 
    os.mkdir(abs_dir_path) 
  except OSError as error: 
    print(error) 
  abs_osmfile_path = abs_dir_path / "newsquadrats.osm"
  # abs_osmgridfile_path = abs_dir_path / "newsquadratsgrid.osm"

  shutil.move("newsquadrats.osm", abs_osmfile_path)
  # shutil.move("newsquadratsgrid.osm", abs_osmgridfile_path)

# Create Garmin map
# https://peatfaerie.medium.com/how-to-create-a-tile-grid-overlay-for-the-garmin-edge-based-on-veloviewer-unexplored-tiles-5b36e7c401bd
  abs_mkgmapfile_path = Path(abs_dir_path).parent / "src" / "ext" / "mkgmap-r4916" / "mkgmap.jar"
# print(abs_mkgmapfile_path)
  mkgmap_output_path = "--output-dir=" + str(abs_dir_path)
  mkgmap_family_id = "--family-id=" + str(int(dir) - 20200000)
  mkgmap_description = "--description=" + "squadrats-" + str(int(dir))
  mkgmap_mapname = "--mapname=" + str(int(dir) + 43040000)
  mkgmap_overview_mapnumber = "--overview-mapnumber=" + str(int(dir) + 43040000 - 1)
  mkgmap_config_path = "--read-config=" + str(missing_squadrats_dir) + "config.txt"
  mkgmap_typ_path = str(missing_squadrats_dir) + "typ.txt"
  mkgmap_style_path = "--style-file=" + str(missing_squadrats_dir) + "mkgmap.style"
  mkgmap_input = "--input-file=" + str(abs_osmfile_path)
  # mkgmap_inputgrid = "--input-file=" + str(abs_osmgridfile_path)

# print(["java", "-ea", "-jar", abs_mkgmapfile_path, mkgmap_config_path, mkgmap_family_id, mkgmap_mapname, mkgmap_overview_mapnumber, mkgmap_style_path, mkgmap_typ_path, mkgmap_description, mkgmap_input, mkgmap_inputgrid, mkgmap_output_path])
# subprocess.run(["java", "-ea", "-jar", abs_mkgmapfile_path, mkgmap_config_path, mkgmap_family_id, mkgmap_mapname, mkgmap_overview_mapnumber, mkgmap_style_path, mkgmap_typ_path, mkgmap_description, mkgmap_input, mkgmap_inputgrid, mkgmap_output_path])
  subprocess.run(["java", "-ea", "-jar", abs_mkgmapfile_path, mkgmap_config_path, mkgmap_family_id, mkgmap_mapname, mkgmap_overview_mapnumber, mkgmap_style_path, mkgmap_typ_path, mkgmap_description, mkgmap_input, mkgmap_output_path])

# Rename map file
  old_name = abs_dir_path / "gmapsupp.img"
  new_name_file = "squadrats-" + str(int(dir)) + "-" + userName + ".img"
  new_name = abs_dir_path / new_name_file
  os.rename(old_name, new_name)
# print(new_name)
  new_img_dir = missing_squadrats_dir + "../../www/missing_squadrats/img/"
  shutil.copy(new_name, new_img_dir)
  return

def cleaning():
  baseDir = Path(__file__).parent.parent.parent
  dateNow = datetime.datetime.now()
  dateDir = dateNow.strftime("%Y%m%d")
  dateDirPath = os.path.join(baseDir, dateDir)
  if os.path.exists(dateDirPath):
    files = os.listdir(dateDirPath)
    print("\n".join(files))
    for fileName in files:
      filePath = os.path.join(dateDirPath, fileName)
      if os.path.isfile(filePath):
        os.remove(filePath)
    os.rmdir(dateDirPath)
  fileToRemove = os.path.join(baseDir, "jobs", "missing_squadrats", "inProcess")
  print("File to removed: " + fileToRemove)
  if os.path.exists(fileToRemove):
    os.remove(fileToRemove)
    print("inProcess removed")
  fileToRemove = os.path.join(baseDir, "jobs", "missing_squadrats", kmlFile)
  print("File to removed: " + fileToRemove)
  if os.path.exists(fileToRemove):
    os.remove(fileToRemove)
    print("kmlFile removed")
  fileToRemove = os.path.join(baseDir, "jobs", "missing_squadrats", kmlFile.replace(".kml", ".sh"))
  print("File to removed: " + fileToRemove)
  if os.path.exists(fileToRemove):
    os.remove(fileToRemove)
    print("shFile removed")
  return

# Arguments

arguments = sys.argv
kmlFile = arguments[1]
userName = arguments[2]
NWlon = float(arguments[3]) # lon, ytile, col, index 1, ~25
NWlat = float(arguments[4]) # lat, xtile, row, index 0, ~60
SElon = float(arguments[5]) # lon, ytile, col, index 1, ~25
SElat = float(arguments[6]) # lat, xtile, row, index 0, ~60

# Variables

logFilePath = "missingSquadrats.log"
logFile = open(logFilePath, "a")  # append mode
zoom = 17
script_dir = os.path.dirname(__file__) + "/" #<-- absolute dir the script is in
missing_squadrats_dir = script_dir
kmlFilePath = missing_squadrats_dir + '../../jobs/missing_squadrats/' + kmlFile
# kmlFilePath = kmlFile
print ('KML file: ', kmlFile, '<BR>\r\n')

nodes = []
ways = []
boundaries = []
interior = []
nodeID = -4306537
wayID = -807654

tic = time.perf_counter()

# Main program

# Calculate squadrats grid corners
gridNW = deg2num(NWlat, NWlon, zoom)
gridSE = deg2num(SElat, SElon, zoom)
print('Grid corners: ', gridNW, ' and ', gridSE, ', dimensions: ', gridSE[1] - gridNW[1], ' and ', gridSE[0] - gridNW[0])
# https://www.programiz.com/python-programming/matrix np.zeros( (rows, cols) )

data = readKmlFile(kmlFilePath)

print('Time after bounding box test: ', time.perf_counter() - tic, ' seconds<BR>\r\n')

gridPoints = MultiPoint(createGridPoints(gridNW, gridSE, zoom))

print('Time after grid creation: ', time.perf_counter() - tic, ' seconds<BR>\r\n')

tilePoints = processGrid(data, gridPoints)

nodes, ways, nodeID, wayID = points2lines(tilePoints, nodeID, wayID)

print('Time before osm write: ', time.perf_counter() - tic, ' seconds<BR>\r\n')

shapely2osm(tilePoints, nodeID, wayID)

print('Time after osm write: ', time.perf_counter() - tic, ' seconds<BR>\r\n')
print('Number of tiles: ', (gridSE[1] - gridNW[1]) *  (gridSE[0] - gridNW[0]))

osm2img()

# Cleaning
# https://www.geeksforgeeks.org/delete-a-directory-or-file-using-python/

cleaning()

print('Total time: ', time.perf_counter() - tic, ' seconds<BR>\r\n')

timeNow = datetime.datetime.now()
timeStamp = timeNow.strftime("%d.%m.%Y %H:%M:%S")
timeTotal = time.perf_counter() - tic

#logFile.write(timeStamp + ";" + userName + ";" + str(timeTotal) + ";" + str(numberOfWays) + "\n")
logFile.write(timeStamp + ";" + userName + ";" + str(timeTotal) + "\n")

logFile.close()

'''
toLog = 'Kml file: ' + kmlFile
logFile.write(toLog + "\n")

toLog = 'Total time: ' + str(time.perf_counter() - tic) + ' seconds'
logFile.write(toLog + "\n---\n")

logFile.close()
'''

