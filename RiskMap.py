from KMLGen import KMLGen

class RiskMap:
    colors = [(252, 3, 3), (252, 32, 3), (252, 61, 3), (252, 128, 3), (252, 198, 3)]
    def __init__(self, regions, numRegions):
        if numRegions >= len(regions):
            numRegions = len(regions)
        
        self.regions = regions[:numRegions]
        self.get_names()
        self.changeColor = [i * int(numRegions/5) for i in range(0, 5)]
    
    def get_names(self):
        for i, region in enumerate(self.regions):
            print(i)
            region.get_locality()

    def generate_kml(self, name="map"):
        gen = KMLGen(name)
        for i, region in enumerate(self.regions):
            c = 0
            for j in self.changeColor:
                if i >= j:
                    c = self.changeColor.index(j)

            color = self.colors[c]
            gen.add_region(i+1, region, color[0], color[1], color[2])
        gen.save(name)
