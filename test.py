from DataStore import DataStore
from watershed import getWatershed

m = DataStore.load('bhopal')

# for l in m:
#     for a in l:
#         print(a)

ls = getWatershed(m, 10)