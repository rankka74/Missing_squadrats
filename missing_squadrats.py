# C:\Users\ollir\AppData\Local\Programs\Python\Python312
# 200k python3 missing_squadrats-beta.py ../../jobs/missing_squadrats/squadrats-2024-03-15.kml Olli 24.068298339843754 60.325588019047146 25.691528320312504 59.90271303178934
# 45k python3 missing_squadrats-beta.py ../../jobs/missing_squadrats/squadrats-2024-03-15.kml Olli 24.486465454101566 60.33204620344783 25.29808044433594 60.12132921812561


import os
from pathlib import Path
import datetime
import subprocess
import sys
import lxml.etree as ET
import numpy as np
import math
import shutil
import time
import shutil

logFilePath = "missingSquadrats.log"
logFile = open(logFilePath, "a")  # append mode

zoom = 17
limitDist = 1000
tic = time.perf_counter()
script_dir = os.path.dirname(__file__) + "/" #<-- absolute dir the script is in
# logFilePath = "/home/10/oranta/missingSquadrats.log"
'''
logFile = open(logFilePath, "a")  # append mode

timeNow = datetime.datetime.now()
toLog = timeNow.strftime("%Y.%m.%d %H:%M:%S")
logFile.write(toLog + "\n")
'''
arguments = sys.argv
# print ('<BR>\r\nArgument List: ', arguments, '<BR>\r\n')
kmlFile = arguments[1]
userName = arguments[2]
NWlon = float(arguments[3])
NWlat = float(arguments[4])
SElon = float(arguments[5])
SElat = float(arguments[6])

def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
  return (xtile, ytile)

# This returns the NW-corner of the square. Use the function with xtile+1 and/or ytile+1 to get the other corners. With xtile+0.5 & ytile+0.5 it will return the center of the tile.   

def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)

# https://stackoverflow.com/questions/33001420/find-destination-coordinates-given-starting-coordinates-bearing-and-distance/33002517#33002517
def getEndpoint(lat1,lon1,bearing,d):
    R = 6371                     #Radius of the Earth
    brng = math.radians(bearing) #convert degrees to radians
    # d = d*1.852                  #convert nautical miles to km
    lat1 = math.radians(lat1)    #Current lat point converted to radians
    lon1 = math.radians(lon1)    #Current long point converted to radians
    lat2 = math.asin( math.sin(lat1)*math.cos(d/R) + math.cos(lat1)*math.sin(d/R)*math.cos(brng))
    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),math.cos(d/R)-math.sin(lat1)*math.sin(lat2))
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    return lat2,lon2

limitNW = getEndpoint(NWlat,NWlon,315,limitDist)
limitSE = getEndpoint(SElat,SElon,135,limitDist)
# print('limitNW: ', limitNW)
# print('limitSE: ', limitSE)

# squadrats grid corners
gridNW = deg2num(NWlat, NWlon, zoom)
gridSE = deg2num(SElat, SElon, zoom)
# print('Grid corners: ', gridNW, ' and ', gridSE)

# https://www.geeksforgeeks.org/how-to-convert-lists-to-xml-in-python/
# we make root element
osm = ET.Element("osm")
osm.set('version', '0.6')
osm.set('generator', 'JOSM')

missing_squadrats_dir = script_dir
kmlFilePath = missing_squadrats_dir + '../../jobs/missing_squadrats/' + kmlFile
#kmlFilePath = kmlFile
print ('KML file: ', kmlFile, '<BR>\r\n')
tree = ET.parse(kmlFilePath)
data = ET.tostring(tree, encoding="unicode", pretty_print=True)
# print ('Data: \r\n', data, '<BR>\r\n')

data = data.split("<name>squadratinhos</name>")[1].split("<name>ubersquadrat</name>")[0]

# calculate number of points
numberOfPoints = 0
for x in data.splitlines():
  if "<coordinates>" in x:
    numberOfPoints = numberOfPoints + x.count(" ") + 1
# print ('Ways: \r\n', numberOfPoints, '<BR>\r\n')
# print('Tilenw: ', tileNW, ' Tilese: ', tileSE)
# nodes = np.zeros((numberOfPoints,3))
# print('Node array size:', nodes.size)
nodeCount = 0
nodeId = -100000
wayId = nodeId - numberOfPoints

wayNumber = 0
for x in data.splitlines():
  if "<coordinates>" in x:
    x = x.split("<coordinates>")[1].split("</coordinates>")[0]
    wayLength = x.count(" ") + 1
    x = x.replace(" ",",").split(",")
    wayNodes = np.zeros((wayLength,1))
    wayPoints = 0
    for y in range(wayLength):
      # lat_deg = float(x.split(" ")[y].split(",")[1])
      lat_deg = float(x[y*2+1])
      # print(SElat, ' < ', lat_deg, ' < ', NWlat, ' and ', NWlon, ' < ', lon_deg, ' < ', SElon)
      if SElat < lat_deg:
        if NWlat > lat_deg:
          # lon_deg = float(x.split(" ")[y].split(",")[0])
          lon_deg = float(x[y*2])
          if NWlon < lon_deg:
            if SElon > lon_deg:
              node = ET.SubElement(osm, "node")
              # Set values for node element
              node.set('id', str(nodeId))
              node.set('visible', 'true')
              node.set('lat', str(lat_deg))
              node.set('lon', str(lon_deg))
              node.text = ''
              # Collect nodeId to array for way creation
              wayNodes[wayPoints,0] = nodeId
              nodeCount = nodeCount + 1
              nodeId = nodeId - 1
              wayPoints = wayPoints + 1
    # print(time.perf_counter() - toc)
    if wayPoints > 0:
      # Initialize way element
      way = ET.SubElement(osm, "way")
      way.set('id', str(wayId))
      way.set('visible', 'true')
      xx = 0
      while xx < wayPoints:
        # Set values for way element
        nd = ET.SubElement(way, "nd")
        nd.set('ref', str(int(wayNodes[xx,0])))
        xx = xx + 1
      tag = ET.SubElement(way, "tag")
      tag.set('k', 'highway')
      tag.set('v', 'primary')
      way.text = ''
      wayId = wayId - 1
      # print('Way number ', wayNumber)
      wayNumber = wayNumber + 1

# Create output dir
dateNow = datetime.datetime.now()
dir = dateNow.strftime("%Y%m%d")
abs_dir_path = Path(__file__).parent.parent.parent / dir
# print('Output dir:', abs_dir_path, '<BR>\r\n')
try: 
    os.mkdir(abs_dir_path) 
except OSError as error: 
    print(error) 
abs_osmfile_path = abs_dir_path / "newsquadrats.osm"
abs_osmgridfile_path = abs_dir_path / "newsquadratsgrid.osm"

# print(abs_osmfile_path)
# subprocess.run(["c:\\Program Files (x86)\\GPSBabel\\gpsbabel.exe", "-w", "-r", "-t", "-i", "gpx", "-f", abs_gpxfile_path, "-o", "osm,tag=highway:primary", "-F", abs_osmfile_path])
tree = ET.ElementTree(osm)
# write the tree into an XML file
# print('Time before osm write: ', time.perf_counter() - tic, ' seconds<BR>\r\n')
# https://stackoverflow.com/questions/52717176/force-elementtree-to-use-closing-tag
# tree.write("newsquadrats.osm", encoding ='utf-8', pretty_print=True, short_empty_elements=False)
tree.write("newsquadrats.osm", encoding ='utf-8', pretty_print=True)
del tree, data

shutil.move("newsquadrats.osm", abs_osmfile_path)

# create squadrats grid

file = open('newsquadratsgrid.osm','w')
file.write("<osm version=\"0.6\" generator=\"JOSM\">\n")

for x in range(gridNW[0], gridSE[0] + 1):
  osmGridWay = "  <way id=\"" + str(wayId) + "\" visible=\"true\">"
  for y in range(gridNW[1], gridSE[1] + 1):
    nodeCoordinates = num2deg(x, y - 1, zoom)
    osmGridRow = "  <node id=\"" + str(nodeId) + "\" visible=\"true\" lat=\"" + str(nodeCoordinates[0]) + "\" lon=\"" + str(nodeCoordinates[1]) + "\"></node>"
    osmGridWay = osmGridWay + "<nd ref=\"" + str(int(nodeId)) + "\"/>"
    # osmGridRow = str(y)
    file.write(osmGridRow + "\n")
    nodeId = nodeId - 1
  osmGridWay = osmGridWay + "<tag k=\"highway\" v=\"secondary \"/></way>"
  file.write(osmGridWay + "\n")
  wayId = wayId - 1

'''
nodeId = nodeId + (gridSE[0] - gridNW[0] + 1) * (gridSE[1] - gridNW[1] + 1)
for x in range(gridNW[0], gridSE[0] + 1):
  osmGridWay = "  <way id=\"" + str(wayId) + "\" visible=\"true\">"
  for y in range(gridNW[1], gridSE[1] + 1):
    osmGridWay = osmGridWay + "<nd ref=\"" + str(int(nodeId)) + "\"/>"
    nodeId = nodeId - 1
  osmGridWay = osmGridWay + "<tag k=\"highway\" v=\"secondary \"/></way>"
  file.write(osmGridWay + "\n")
  wayId = wayId - 1
'''

# print(abs_osmfile_path)
# subprocess.run(["c:\\Program Files (x86)\\GPSBabel\\gpsbabel.exe", "-w", "-r", "-t", "-i", "gpx", "-f", abs_gpxfile_path, "-o", "osm,tag=highway:primary", "-F", abs_osmfile_path])
# write the tree into an XML file
# print('Time before osm write: ', time.perf_counter() - tic, ' seconds<BR>\r\n')
# https://stackoverflow.com/questions/52717176/force-elementtree-to-use-closing-tag
# tree.write("newsquadrats.osm", encoding ='utf-8', pretty_print=True, short_empty_elements=False)
numberOfWays = (gridSE[0] - gridNW[0]) * (gridSE[1] - gridNW[1])
numberOfWrites = int(numberOfWays / 8000)
stepOfWrites = int((gridSE[0] - gridNW[0]) / numberOfWrites)
print('Ways: ', numberOfWays, ', writes: ', numberOfWrites, ' , step: ', stepOfWrites, ' <BR>\r\n')

# print(nodeId, '\r\n')
nodeId = nodeId + (gridSE[0] - gridNW[0] + 1) * (gridSE[1] - gridNW[1] + 1)
# print(nodeId, '\r\n')

loopCountY = 0
for y in range(gridNW[1], gridSE[1] + 1):
  loopCountX = 0
  osmGridWay = "  <way id=\"" + str(wayId) + "\" visible=\"true\">"
  for x in range(gridNW[0], gridSE[0] + 1):
    osmGridWay = osmGridWay + "<nd ref=\"" + str(int(nodeId) - loopCountX * (gridSE[1] + 1 - gridNW[1]) - loopCountY) + "\"/>"
    loopCountX = loopCountX + 1
  osmGridWay = osmGridWay + "<tag k=\"highway\" v=\"secondary \"/></way>"
  file.write(osmGridWay + "\n")
  loopCountY = loopCountY + 1
  wayId = wayId - 1

file.write("</osm>\n")
file.close()

# print('osm file done: ', abs_osmgridfile_path, '\r\n')

shutil.move("newsquadratsgrid.osm", abs_osmgridfile_path)

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
mkgmap_inputgrid = "--input-file=" + str(abs_osmgridfile_path)

print(["java", "-ea", "-jar", abs_mkgmapfile_path, mkgmap_config_path, mkgmap_family_id, mkgmap_mapname, mkgmap_overview_mapnumber, mkgmap_style_path, mkgmap_typ_path, mkgmap_description, mkgmap_input, mkgmap_inputgrid, mkgmap_output_path])
subprocess.run(["java", "-ea", "-jar", abs_mkgmapfile_path, mkgmap_config_path, mkgmap_family_id, mkgmap_mapname, mkgmap_overview_mapnumber, mkgmap_style_path, mkgmap_typ_path, mkgmap_description, mkgmap_input, mkgmap_inputgrid, mkgmap_output_path])

# Rename map file
old_name = abs_dir_path / "gmapsupp.img"
new_name_file = "squadrats-" + str(int(dir)) + "-" + userName + ".img"
new_name = abs_dir_path / new_name_file
os.rename(old_name, new_name)
# print(new_name)
new_img_dir = missing_squadrats_dir + "../../www/missing_squadrats/img/"
shutil.copy(new_name, new_img_dir)
#shutil.rmtree(abs_dir_path)
#os.remove(kmlFilePath)

# Cleaning
# https://www.geeksforgeeks.org/delete-a-directory-or-file-using-python/
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

print('Total time: ', time.perf_counter() - tic, ' seconds<BR>\r\n')

timeNow = datetime.datetime.now()
timeStamp = timeNow.strftime("%d.%m.%Y %H:%M:%S")
timeTotal = time.perf_counter() - tic

logFile.write(timeStamp + ";" + userName + ";" + str(timeTotal) + ";" + str(numberOfWays) + "\n")

logFile.close()

'''
toLog = 'Kml file: ' + kmlFile
logFile.write(toLog + "\n")

toLog = 'Total time: ' + str(time.perf_counter() - tic) + ' seconds'
logFile.write(toLog + "\n---\n")

logFile.close()
'''
