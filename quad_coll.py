from PIL import ImageDraw

MAX_DEPTH = 16
MIN_SIZE = 4
MIN_RATIO = .05
MIN_OPACITY = .1

class QuadTree:
    def __init__(self):
        self.NW = None
        self.NE = None
        self.SW = None
        self.SE = None
        self.full = False

    def isLeaf(self):
        return (self.NW == None
            and self.NE == None
            and self.SW == None
            and self.SE == None)

    def getNumNodes(self):
        return self.__countNodes(True)

    def getNumLeafNodes(self):
        return self.__countNodes(False)

    def __countNodes(self, countAllNodes=True):
        if (self.isLeaf()):
            return 1
        else:
            if (countAllNodes):
                count = 1
            else:
                count = 0
            if (self.NW != None):
                count = count + self.NW.__countNodes(countAllNodes)
            if (self.NE != None):
                count = count + self.NE.__countNodes(countAllNodes)
            if (self.SW != None):
                count = count + self.SW.__countNodes(countAllNodes)
            if (self.SE != None):
                count = count + self.SE.__countNodes(countAllNodes)
            return count

def checkFill(img):
    fullCount = 0
    data = img.getdata()
    for px in data:
        if (px[3]/255.0 > MIN_OPACITY):
            fullCount = fullCount + 1
    return fullCount/float(len(data))

def calcError(img, tree):
    d = {'imgPixels': 0, 'treePixels': 0, 'falsePositives': 0, 'falseNegatives': 0}
    __calcError(img, tree, d)
    return d

def __calcError(img, curNode, d):
    width = img.size[0]
    height = img.size[1]
    nodePixels = width*height
    imgPixels = nodePixels*checkFill(img)

    d['imgPixels'] = d['imgPixels'] + imgPixels
    d['treePixels'] = d['treePixels'] + nodePixels

    if (curNode.isLeaf()):
        if (curNode.full):
            d['falsePositives'] = d['falsePositives'] + nodePixels - imgPixels
        else:
            d['falseNegatives'] = d['falseNegatives'] + imgPixels
    else:
        midx = width/2
        midy = height/2

        imgNW = img.crop((0, 0, midx, midy))
        __calcError(imgNW, curNode.NW, d)

        imgNE = img.crop((midx, 0, width, midy))
        __calcError(imgNE, curNode.NE, d)

        imgSW = img.crop((0, midy, midx, height))
        __calcError(imgSW, curNode.SW, d)

        imgSE = img.crop((midx, midy, width, height))
        __calcError(imgSE, curNode.SE, d)


def makeTree(img):
    tree = QuadTree()
    __makeTree(img, tree, 0)
    return tree

def __makeTree(img, curNode, depth):

    width = img.size[0]
    height = img.size[1]
    imgFill = checkFill(img)

    if (depth < MAX_DEPTH
        and width > MIN_SIZE
        and height > MIN_SIZE):
        if (imgFill < MIN_RATIO):
            curNode.full = False
        elif (imgFill > (1 - MIN_RATIO)):
            curNode.full = True
        else:
            midx = width/2
            midy = height/2

            imgNW = img.crop((0, 0, midx, midy))
            curNode.NW = QuadTree()
            __makeTree(imgNW, curNode.NW, depth + 1)

            imgNE = img.crop((midx, 0, width, midy))
            curNode.NE = QuadTree()
            __makeTree(imgNE, curNode.NE, depth + 1)

            imgSW = img.crop((0, midy, midx, height))
            curNode.SW = QuadTree()
            __makeTree(imgSW, curNode.SW, depth + 1)

            imgSE = img.crop((midx, midy, width, height))
            curNode.SE = QuadTree()
            __makeTree(imgSE, curNode.SE, depth + 1)
    else:
        curNode.full = (imgFill > MIN_RATIO)

def printTree(tree, width, height):
    __printTree(tree, 0, 0, 0, width, height)

def __printTree(curNode, depth, x, y, maxx, maxy):
    if (curNode == None):
        return

    if (curNode.isLeaf() and curNode.full):
        print depth*'  ' + 'FULL x: %d, y: %d, maxx: %d, maxy: %d' % (x, y, maxx, maxy)
    else:
        print depth*'  ' + 'x: %d, y: %d, maxx: %d, maxy: %d' % (x, y, maxx, maxy)

        midx = (x + maxx)/2
        midy = (y + maxy)/2

        __printTree(curNode.NW, depth + 1, x, y, midx, midy)
        __printTree(curNode.NE, depth + 1, midx, y, maxx, midy)
        __printTree(curNode.SW, depth + 1, x, midy, midx, maxy)
        __printTree(curNode.SE, depth + 1, midx, midy, maxx, maxy)

def drawTree(img, tree, drawEmptySpace=False):
    draw = ImageDraw.Draw(img)
    __drawTree(draw, tree, 0, 0, img.size[0], img.size[1], drawEmptySpace)

def __drawTree(imgDraw, curNode, x, y, maxx, maxy, drawEmptySpace):
    if (curNode == None):
        return

    if (curNode.isLeaf()):
        if (curNode.full):
            imgDraw.rectangle([x, y, maxx, maxy], outline=(255, 0, 0, 255), fill=(255, 0, 0, 128))
        elif (drawEmptySpace):
            imgDraw.rectangle([x, y, maxx, maxy], outline=(0, 255, 0, 255), fill=(0, 255, 0, 128))
    else:
        midx = (x + maxx)/2
        midy = (y + maxy)/2

        __drawTree(imgDraw, curNode.NW, x, y, midx, midy, drawEmptySpace)
        __drawTree(imgDraw, curNode.NE, midx, y, maxx, midy, drawEmptySpace)
        __drawTree(imgDraw, curNode.SW, x, midy, midx, maxy, drawEmptySpace)
        __drawTree(imgDraw, curNode.SE, midx, midy, maxx, maxy, drawEmptySpace)




