import cv2
import numpy as np
from RiskMapRegion import RiskMapRegion

def func(x):
    return (-x.risk, -x.area)

def getWatershed(data, w):
    height = np.array(data)
    image = np.zeros(height.shape)
    for i in range(len(data)):
        for j in range(len(data[0])):
            height[i][j] = data[i][j].elevation
    maximum = np.amax(height)
    minimum = np.amin(height)
    numberOfBits = 16
    interval = (maximum - minimum) / (pow(2, numberOfBits) - 1)
    for i in range(len(height)):
        for j in range(len(height[0])):
            image[i][j] = int( data[i][j].getRisk(minimum, maximum) * (pow(2, numberOfBits) - 1))

    image = image.astype('uint8') * 255

    # image = cv2.bitwise_not(image)
    # image = resizeimage(image, 1000)
    image3 = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    ret, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # noise removal
    kernel = np.ones((3, 3), np.uint8)

    # sure background area
    sure_bg = cv2.dilate(thresh, kernel, iterations=3)

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.1 * dist_transform.max(), 255, 0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)

    # Add one to all labels so that sure background is not 0, but 1
    markers = markers + 1

    # Now, mark the region of unknown with zero
    markers[unknown == 255] = 0
    markers = cv2.watershed(image3, markers)
    diff = []
    for m in markers:
        for a in m:
            if not a in diff:
                diff.append(a)

    image3[markers == -1] = [255, 0, 0]
    print("YO")

    # Map to store region wise location objects
    regions = getRegions(markers, data)

    # Map to store region boundary location objects
    regionBoundary = findboundary2(markers, data)

    # Map to store regions and there relative sizes
    sizeFactor = {}

    # Size list
    sizeList = {}
    
    # Map to Store Average Depths
    avgDepth = {}

    # Map to store the centers of the regions
    centers = {}
    print("YO")
    maxSize = 0
    for k in regions:
        # Find maximum size region
        if k not in sizeFactor:
            sizeFactor[k] = float(len(regions[k]))
            maxSize = max(maxSize, sizeFactor[k])
        sizeList[k] = len(regions[k])
        
        # Find the center of the region i,e, the minimum depth region
        minDepth = regions[k][0]

        # Depth wise classification
        depthSum = 0
        for val in regions[k]:
            if minDepth.elevation > val.elevation:
                minDepth = val
            depthSum = depthSum + val.elevation
        centers[k] = minDepth

        # Normalise the depth
        avgDepth[k] = depthSum/len(regions[k])
    print("YO")
    # Normalize the size factors with respect to greatest size region
    for k in sizeFactor:
        sizeFactor[k] = sizeFactor[k] / maxSize

    maxDepth = avgDepth[list(avgDepth.keys())[0]]
    for k in avgDepth:
        maxDepth = max(maxDepth, avgDepth[k])
    for k in avgDepth:
        avgDepth[k] = avgDepth[k] / maxDepth

    factor1 = 0.5
    factor2 = 0.5
    riskFactor = {}
    for k in regions:
        riskFactor[k] = factor1*(1-avgDepth[k]) + factor2*sizeFactor[k]
    print("YO")
    riskObjects = []
    rs = []
    for k in regions:
        if k == -1:
            continue
        risk = riskFactor[k]
        area = pow((pow(sizeList[k], 0.5) * w)/1000, 2)
        rs.append((-risk, -area, k))

    rs.sort()
    rss = rs[:w]
    rb = {}
    for r in rss:
        rb[r[2]] = regionBoundary[r[2]]
    
    print("YO")
    sb = sort_boundaries(rb, data)
    for r in rss:
        riskObjects.append(RiskMapRegion(centers[r[2]],sb[r[2]],risk,area))

    return riskObjects


def getRegions(markers, locations):
    maps = {}
    for i in range(len(markers)):
        for j in range(len(markers[0])):
            if markers[i][j] == -1:
                continue
            if not markers[i][j] in maps:
                maps[markers[i][j]] = [locations[i][j]]
            else:
                maps[markers[i][j]].append(locations[i][j])
    return maps

def findboundary2(markers, location):
    boundaries = {}
    
    p = [(0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]
    n = len(markers)
    m = len(markers[0])
    for i in range(n):
        for j in range(m):
            if markers[i][j] == -1:
                for b in p:
                    if isValid(i+b[0], j+b[1], n, m) and markers[i+b[0]][j+b[1]] != -1:
                        v = markers[i+b[0]][j+b[1]]
                        if v not in boundaries:
                            boundaries[v] = [(i, j)]
                        else:
                            boundaries[v].append((i, j))
    return boundaries
    

def sort_boundaries(boundaries, location):
    locs = {}
    for i, k in enumerate(boundaries):
        print(i)
        arr = boundaries[k]
        done = [arr[0]]
        arr.remove(arr[0])

        while len(arr) > 0:
            n = done[-1]
            m = dist(n, arr[0])
            j = 0
            for i in range(len(arr)):
                v = dist(n, arr[i])
                if v < m:
                    j = i
                    m = v
            done.append(arr[j])
            arr.remove(arr[j])

        locs[k] = [location[a[0]][a[1]] for a in done]
    return locs

def dist(a, b):
    return pow((a[0] - b[0])**2 + (a[1] - b[1])**2, 0.5)

def isValid(x, y, n ,m):
    return 0 <= x < n and 0 <= y < m

def findboundary(markers, location):
    maps = {}
    doneRegions = [-1]
    n = len(markers)
    m = len(markers[0])
    for i in range(n):
        for j in range(m):
            if (markers[i][j] not in doneRegions and isBoundaryPixel(markers, i, j, n, m)):
                maps[markers[i][j]] = findRegionBound(markers, i, j, location)
                doneRegions.append(markers[i][j])
    return maps


def findRegionBound(markers, i, j, location):
    dir = [[1, 0, -1, 0, 1, -1, -1, 1], 
            [0, 1, 0, -1, 1, 1, -1, -1]]
    n = len(markers)
    m = len(markers[0])
    ret = [location[i][j]]
    visited = [(i, j)]
    while True:
        a = True
        for k in range(len(dir[0])):
            x = i + dir[0][k]
            y = j + dir[1][k]
            
            if (x, y) not in visited and markers[x][y] == markers[i][j] and isBoundaryPixel(markers, x, y, n, m):
                visited.append((x, y))
                ret.append(location[x][y])
                i = x
                j = y
                a = False
                break
        if a:
            return ret


def isBoundaryPixel(markers, i, j, n, m):
    dir = [[0, 1, 1, 1, 0, -1, -1, -1], 
            [1, 1, 0, -1, -1, -1, 0, 1]]
    flag = 0
    for k in range(len(dir[0])):
        x = i + dir[0][k]
        y = j + dir[1][k]
        if markers[x][y] != markers[i][j]:
            return True
    return False


def resizeimage(image, W):
    height, width = image.shape
    imgScale = W / width
    newX, newY = image.shape[1] * imgScale, image.shape[0] * imgScale
    return cv2.resize(image, (int(newX), int(newY)))


if __name__ == '__main__':
    getWatershed(np.random.random((100, 100)))
