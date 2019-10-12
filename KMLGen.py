import simplekml
from RiskMapRegion import RiskMapRegion
from Location import Location

class KMLGen:
    def __init__(self, name):
        self.kml = simplekml.Kml()
        self.kml.document.name = name

    def add_region(self, i, region, r, g, b):
        name = "{}. {}".format(i, region.name)
        pnt = self.kml.newpoint(name=name)
        pnt.description = "Risk: {}\nArea: {} Km2".format(round(region.risk, 2), round(region.area, 2))
        pnt.coords = [(region.center.lon, region.center.lat)]
        pnt.style.labelstyle.color = simplekml.Color.rgb(r, g, b)

        pol = self.kml.newpolygon(name=name)
        ob = []
        for rg in region.region:
            ob.append((rg.lon, rg.lat))
        pol.outerboundaryis = ob
        pol.style.polystyle.color = simplekml.Color.rgb(r, g, b, a=100)

    def save(self, name=None):
        if name is None:
            name = self.kml.document.name
        self.kml.save("maps/" + name + ".kml")

if __name__ == "__main__":
    g = KMLGen("map")
    l1 = Location(23.21227, 77.3923)
    l2 = Location(23.22152, 77.40453)
    l3 = Location(23.21726, 77.41741)
    l4 = Location(23.20453, 77.41685)
    r = RiskMapRegion(
        center=Location(23.214309, 77.404280),
        region=[l1, l2, l3, l4],
        risk=0.5,
        area=100,
    )
    r.get_locality()
    g.add_region(1, r, 252, 3, 3)
    g.save()