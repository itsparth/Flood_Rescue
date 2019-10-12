from DataStore import DataStore
from LocationParser import LocationParser
from ElevationParser import ElevationParser
from Location import Location
from watershed import getWatershed
from RiskMap import RiskMap
import time
import requests

_BASE_URL = "https://us1.locationiq.com/v1/reverse.php?key=a172c9cffa6540&lat={}&lon={}&format=json&zoom=10"

resp = requests.get(_BASE_URL.format(21.82706108, 75.613033)).json()["boundingbox"]
box = resp[0] + "," + resp[2] + "," + resp[1] + "," + resp[3]

coords = str(box).split(',')
first = Location(float(coords[0]), float(coords[1]))
second = Location(float(coords[2]), float(coords[3]))

# first = Location(27.93736, 85.11241)
# second = Location(27.57034, 85.53813)

locParser = LocationParser(first, second, accuracy=100)
locParser.parse()

elevParser = ElevationParser(locParser.grid)

DataStore.save(elevParser.grid, name="kgn")

bpl = DataStore.load('kgn')
l = getWatershed(bpl, 1000)

m = RiskMap(l, 10)
m.generate_kml(name='kgn')