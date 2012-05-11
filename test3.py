import quad_tree
from PIL import Image
from PIL import ImageDraw
from random import randrange

class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self):
        return 'Rect(%d, %d, %d, %d)' % (self.x, self.y, self.width, self.height)

def printTree(tree, depth):
    print depth*'  ' + 'x: %d, y: %d, right: %d, bottom: %d' % (tree.left, tree.top, tree.right, tree.bottom)
    if (len(tree.objects) > 0):
        print depth*'  ' + str(tree.objects)
    if (tree.NW):
        printTree(tree.NW, depth+1)
    if (tree.NE):
        printTree(tree.NE, depth+1)
    if (tree.SW):
        printTree(tree.SW, depth+1)
    if (tree.SE):
        printTree(tree.SE, depth+1)

def drawTree(tree, draw):
    draw.rectangle((tree.left+50, tree.top+50, tree.right+50, tree.bottom+50), outline=(0, 0, 0, 255))
    if (tree.NW):
        drawTree(tree.NW, draw)
    if (tree.NE):
        drawTree(tree.NE, draw)
    if (tree.SW):
        drawTree(tree.SW, draw)
    if (tree.SE):
        drawTree(tree.SE, draw)

tree = quad_tree.QuadTree(0, 0, 320, 240)

img = Image.new('RGBA', (420, 340))
img.putdata(420*340*[(255, 255, 255, 255)])
draw = ImageDraw.Draw(img)

for i in range(500):
    x0 = randrange(0, 320)
    y0 = randrange(0, 240)
    x1 = randrange(x0, 320)
    y1 = randrange(y0, 240)
    draw.rectangle((x0+50, y0+50, x1+50, y1+50), outline=(255, 0, 0, 255), fill=(255, 162, 0, 12))
    r = Rect(x0, y0, x1 - x0, y1 - y0)
    print r
    tree.addObject(r)

printTree(tree, 0)
drawTree(tree, draw)

img.show()