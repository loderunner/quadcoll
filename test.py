from PIL import Image
from PIL import ImageDraw
from PIL import ImageChops
import quad_coll

depths = [4, 8, 16]
sizes = [2, 4, 6, 8, 10]
ratios = [.01, .05, .1, .25]
opacities = [.1, .25, .5, .75, .9]
n = 0

img = Image.open('quarter.png')
for d in depths:
    quad_coll.MAX_DEPTH = d
    for s in sizes:
        quad_coll.MIN_SIZE = s
        for r in ratios:
            quad_coll.MIN_RATIO = r
            for o in opacities:
                quad_coll.MIN_OPACITY = o

                tree = quad_coll.makeTree(img)

                img2 = Image.new('RGBA', img.size)
                quad_coll.drawTree(img2, tree)
                draw = ImageDraw.Draw(img2)
                draw.text((0, 0), 'max tree depth: %d' % d)
                draw.text((0, 10), 'min node size: %d pixels' % s)
                draw.text((0, 20), 'min node fill ratio: %f pixels' % r)
                draw.text((0, 30), 'min filled pixel opactiy:%f alpha' % o)

                ImageChops.composite(img2, img, img2).save('text%02d.png' % n)
                n = n + 1
