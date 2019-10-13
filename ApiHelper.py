import requests
from Location import Location
from LocationParser import LocationParser
from ElevationParser import ElevationParser
from DataStore import DataStore
from watershed import getWatershed
from RiskMap import RiskMap

class APIHelper:
    _BASE_URL = "https://us1.locationiq.com/v1/reverse.php?key=a172c9cffa6540&lat={}&lon={}&format=json&zoom=10"
    task = "1/3"
    status = "Starting..."
    done = "0%"
    def get_risk_map(self, location=None, box=None, name="map", accuracy=10):
        if location is not None:
            locs = location.split(',')
            resp = requests.get(self._BASE_URL.format(locs[0], locs[1])).json()["boundingbox"]
            box = resp[0] + "," + resp[2] + "," + resp[1] + "," + resp[3]

        coords = str(box).split(',')
        first = Location(float(coords[0]), float(coords[1]))
        second = Location(float(coords[2]), float(coords[3]))

        locParser = LocationParser(first, second, accuracy=accuracy)
        locParser.parse()

        elevParser = ElevationParser(locParser.grid)

        DataStore.save(elevParser.grid, name=name)

        data = DataStore.load(name)
        s = getWatershed(data, 100)

        m = RiskMap(s, 10)
        m.generate_kml(name=name)
    
    def get_progress(self, id):
        pass

    def download(self, id):
        pass


