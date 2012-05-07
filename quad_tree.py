MAX_DEPTH = 6
MIN_SIZE = 50

class QuadTree:
    def __init__(self, maxDepth=MAX_DEPTH, minSize=MIN_SIZE):
        self.maxDepth = maxDepth
        self.minSize = minSize
        self.NW = None
        self.NE = None
        self.SW = None
        self.SE = None
        self.objList = []

    def addobj(self, obj, width, height):
        self.__addobj(obj, 0, 0, width, height, 0)

    def __addobj(self, obj, x, y, width, height, depth):

        right = x + width
        bottom = y + height
        objRight = obj.x + obj.width
        objBottom = obj.y + obj.height

        # max depth or obj covers quad => add to list
        if ((depth >= self.maxDepth)
            || ((x >= obj.x && y >= obj.y && right <= objRight && bottom <= objBottom))):
            self.objList.append(obj)

        midx = x + width/2
        midy = y + height/2
        if (obj.x >= x && obj.x + width <= midx && obj.y)
