from DataStore import DataStore
from LocationParser import LocationParser
from ElevationParser import ElevationParser
from Location import Location
from watershed import getWatershed
from RiskMap import RiskMap
import time
import requests

# _BASE_URL = "https://us1.locationiq.com/v1/reverse.php?key=a172c9cffa6540&lat={}&lon={}&format=json&zoom=10"

# resp = requests.get(_BASE_URL.format(21.82706108, 75.613033)).json()["boundingbox"]
# box = resp[0] + "," + resp[2] + "," + resp[1] + "," + resp[3]

# coords = str(box).split(',')
# first = Location(float(coords[0]), float(coords[1]))
# second = Location(float(coords[2]), float(coords[3]))
first_lat = float(input("Enter first latitude:"))
first_lon = float(input("Enter first longitude:"))

second_lat = float(input("Enter second latitude:"))
second_lon = float(input("Enter second longitude:"))

first = Location(first_lat, first_lon)
second = Location(second_lat, second_lon)

name = input("Enter city name:")
accuracy = int(input("Enter accuracy in meteres:"))

locParser = LocationParser(first, second, accuracy=accuracy)
locParser.parse()

elevParser = ElevationParser(locParser.grid)

DataStore.save(elevParser.grid, name=name)

data = DataStore.load(name)
s = getWatershed(data, 100)

m = RiskMap(s, 10)
m.generate_kml(name=name)