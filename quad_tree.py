MAX_DEPTH = 6
MIN_SIZE = 50

class QuadTree:
    def __init__(self, left, top, right, bottom, maxDepth=MAX_DEPTH, minSize=MIN_SIZE):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.maxDepth = maxDepth
        self.minSize = minSize
        self.NW = None
        self.NE = None
        self.SW = None
        self.SE = None
        self.objects = []

    def addObject(self, obj):
        print 'adding ' + str(obj)
        self.__addObject(obj, 0)

    def __addObject(self, obj, depth):
        # object fits in a quadrant
        if (depth < self.maxDepth):
            midx = (self.left + self.right)/2
            midy = (self.top + self.bottom)/2
            objRight = obj.x + obj.width
            objBottom = obj.y + obj.height
            if (obj.x >= self.left and objRight < midx):
                if (obj.y >= self.top and objBottom < midy):
                    # print depth*'  ' + 'in NW quadrant'
                    if (self.NW == None):
                        self.NW = QuadTree(self.left, self.top, midx, midy, self.maxDepth, self.minSize)
                    self.NW.__addObject(obj, depth+1)
                    return
                elif (obj.y >= midy and objBottom < self.bottom):
                    # print depth*'  ' + 'in SW quadrant'
                    if (self.SW == None):
                        self.SW = QuadTree(self.left, midy, midx, self.bottom, self.maxDepth, self.minSize)
                    self.SW.__addObject(obj, depth+1)
                    return
            elif (obj.x >= midx and objRight < self.right):
                if (obj.y >= self.top and objBottom < midy):
                    # print depth*'  ' + 'in NE quadrant'
                    if (self.NE == None):
                        self.NE = QuadTree(midx, self.top, self.right, midy, self.maxDepth, self.minSize)
                    self.NE.__addObject(obj, depth+1)
                    return
                elif (obj.y >= midy and objBottom < self.bottom):
                    # print depth*'  ' + 'in SE quadrant'
                    if (self.SE == None):
                        self.SE = QuadTree(midx, midy, self.right, self.bottom, self.maxDepth, self.minSize)
                    self.SE.__addObject(obj, depth+1)
                    return

        # print depth*'  '+'added'
        self.objects.append(obj)
