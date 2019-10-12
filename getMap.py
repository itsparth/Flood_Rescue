import urllib.request

def getMap():
    url = "http://www.mapquestapi.com/staticmap/v4/getmap"
    url += "?key=on8TAGOqbsmKnxvqk9D572bnRDOv2Pm0"
    url += "&size=300,400&bestfit=23.21312,77.40763,23.21224,77.4097&margin=1"
    print(url)
    urllib.request.urlretrieve(url, "map.jpg")

getMap()