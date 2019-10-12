from Location import Location

class LocationParser:
    _DELTA = 0.00001

    def __init__(self, topLeft, bottomRight, accuracy=10):
        self.topLeft, self.bottomRight = self.parseLatLong(topLeft, bottomRight)
        self.accuracy = accuracy

    def parseLatLong(self, topLeft, bottomRight):
        minLat = min(topLeft.lat, bottomRight.lat)
        maxLat = max(topLeft.lat, bottomRight.lat)
        minLon = min(topLeft.lon, bottomRight.lon)
        maxLon = max(topLeft.lon, bottomRight.lon)

        return Location(minLat, minLon), Location(maxLat, maxLon)

    def parse(self):
        self.grid = []
        currLat = self.topLeft.lat
        while currLat <= self.bottomRight.lat:
            currLon = self.topLeft.lon
            temp = []
            while currLon <= self.bottomRight.lon:
                temp.append(Location(currLat, currLon))
                currLon += self._DELTA * self.accuracy
            
            self.grid.append(temp)
            currLat += self._DELTA * self.accuracy
    
    