# About The Project
Create a Garmin compatible map image from the [Squadrats.com](http://www.squadrats.com/) kml file.

# Getting Started
## Prerequisites
You need a working python installation to run the script.

## Installation
1. Clone the repo
```
git clone https://github.com/rankka74/Missing_squadrats.git
```
2. Install necessary python libraries eiter system wise or as a virtual environment
```
sys
os
time
math
shapely.geometry
datetime
pathlib
shutil
subprocess
```
3. Modify path variables to match your system
4. Download and uncompress [mkgmap](https://www.mkgmap.org.uk/)

# Usage
```
python3 missing_squadrats.py kml-file userID NWlon NWlat SElon SElat
```
## Example
```
python3 missing_squadrats.py squadrats-2026-02-01.kml Olli 24.859027260564833 60.220602974148186 24.947346246430854 60.197660629350736
```

# Roadmap
- [ ] Add optional grid for whole map area
- [ ] User configurable tile line color and width
- [ ] Add an option to make a map of squadrats (zoom level 14)
