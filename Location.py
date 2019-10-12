
class Location:
    def __init__(self, lat, lon, elevation=None):
        self.lat = round(lat, 6)
        self.lon = round(lon, 6)
        self.elevation = elevation

    def __str__(self):
        return "Location({},{},{})".format(self.lat, self.lon, self.elevation)

    def getLatLon(self):
        return "{},{}".format(self.lat, self.lon)

    def getRisk(self, minE, maxE):
        return (self.elevation - minE) / (maxE - minE)