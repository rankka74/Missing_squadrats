# About The Project
Create a Garmin compatible map image from the [Squadrats.com](http://www.squadrats.com/) kml file.

# Getting Started

## Docker

The easiest way to run the project is with Docker.

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) with the Compose plugin

### Run
```
git clone https://github.com/rankka74/Missing_squadrats.git
cd Missing_squadrats
docker compose up --build
```

Open http://localhost:8000 in your browser.

### How it works inside Docker
- **Web GUI** is served by the PHP built-in server on port 8000.
- Submitting the form uploads the KML file and runs `missing_squadrats.py` synchronously — the page shows "Done!" when the `.img` file is ready.
- Generated `.img` files, the job queue, and the log are stored in named Docker volumes so they survive container restarts.

### Volumes
| Volume | Contents |
|---|---|
| `img-files` | Generated Garmin `.img` files |
| `job-queue` | Pending and in-progress jobs |
| `oranta-data` | Log file and map-number counter |

To reset everything: `docker compose down -v`

---

## Manual installation

### Prerequisites
You need a working Python installation to run the script.

### Installation
1. Clone the repo
```
git clone https://github.com/rankka74/Missing_squadrats.git
```
2. Install necessary python libraries either system wide or as a virtual environment
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

# Inspiration
- [How to create a tile grid overlay for the Garmin Edge based on VeloViewer unexplored tiles](https://peatfaerie.medium.com/how-to-create-a-tile-grid-overlay-for-the-garmin-edge-based-on-veloviewer-unexplored-tiles-5b36e7c401bd)
- [https://github.com/Myrtillus/arkiruudut](https://github.com/Myrtillus/arkiruudut)
- [https://colab.research.google.com/drive/1jU3_k32zwaM1d1ftZv-9XOaO_dHWCWr_](https://colab.research.google.com/drive/1jU3_k32zwaM1d1ftZv-9XOaO_dHWCWr_)
- [https://github.com/pailakka/mtk2garmin](https://github.com/pailakka/mtk2garmin)
- [https://www.mail-archive.com/mkgmap-dev@lists.mkgmap.org.uk/msg01125.html](https://www.mail-archive.com/mkgmap-dev@lists.mkgmap.org.uk/msg01125.html)
