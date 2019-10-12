import requests
from Location import Location
class RiskMapRegion:
    _BASE_URL = "https://us1.locationiq.com/v1/reverse.php?key=a172c9cffa6540&lat={}&lon={}&format=json"
    
    def __init__(self, center, region, risk, area):
        self.center = center
        self.region = region
        self.risk = risk
        self.area = area
    
    def get_locality(self):
        resp = requests.get(self._BASE_URL.format(self.center.lat, self.center.lon))
        self.name = resp.json()['display_name']


if __name__ == "__main__":
    r = RiskMapRegion(
        center=Location(23.214309, 77.404280),
        region=None,
        risk=None,
        area=None,
    )

    r.get_locality()