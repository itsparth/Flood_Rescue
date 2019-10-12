import requests
from threading import Thread
import time

class ElevationParser:
    BASE_URL = "https://api.jawg.io/elevations/locations?access-token=3jlNWopSNvLYx1dxI6TANMF6upCn1TeJ5SycNAM176hSbyBuyo6vO01y9GmCOI76"

    def __init__(self, grid, threads=1, callback=None):
        self.grid = grid
        self.done = False
        self.callback = callback
        #self._manager(count=threads)
        self._worker2()

    def _manager(self, count):
        threads = []
        diff = int(len(self.grid) / count)
        for i in range(count):
            k = min(diff, len(self.grid) - i * diff)
            t = Thread(target=self._worker, args=[i*diff, i*diff+k])
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

        self.done = True
        if self.callback is not None:
            self.callback()

    def _worker2(self):
        locs = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                locs.append((i, j))
                if len(locs) == 500:
                    self._get_elevation(locs)
                    locs = []
                    done = i * len(self.grid[0]) + j
                    print("{}/{}".format(done,len(self.grid)*len(self.grid[0])))
        if len(locs) != 0:
            self._get_elevation(locs)

    def _get_elevation(self, locs):
        locations = self.grid[locs[0][0]][locs[0][1]].getLatLon()
        for loc in locs[1:]:
            locations += "|" + self.grid[loc[0]][loc[1]].getLatLon()
        retry = 4
        while retry > 0:
            retry -= 1
            try:
                import json
                response = requests.post(self.BASE_URL,
                data=json.dumps({"locations": str(locations)}),
                headers={
                    'content-type': 'application/json', 
                    'accept': 'application/json'}, timeout=10)
                if response.status_code != 200:
                    print(response.text)
                    raise Exception("Failed")
                self._fill(locs, response.json())
                time.sleep(1)
                return True

            except Exception as e:
                print(e)
            time.sleep(1)

    def _fill(self, locs, rawJson):
        for i, loc in enumerate(rawJson):
            self.grid[locs[i][0]][locs[i][1]].elevation = int(loc['elevation'])