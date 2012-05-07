from PIL import Image
from PIL import ImageDraw
from PIL import ImageChops

import quad_coll
import os

depths = [4, 6, 8, 12, 14, 16]
sizes = [2, 4, 6, 8, 10]
ratios = [.01, .05, .1, .25]
opacities = [.1, .25, .5, .75, .9]

for f in os.listdir('.'):
    try:
        img = Image.open(f)
    except IOError:
        pass
    else:
        idx = f.rfind('.')
        if (idx == -1):
            imgName = f
            imgExtension = ''
        else:
            imgName = f[:idx]
            imgExtension = f[idx:]

        dirName = imgName + '_test'
        try:
            os.mkdir(dirName)
        except OSError as e:
            if (e.errno != 17):
                raise e

        n = 0
        csv = file(dirName + '/' + imgName + '_trees.csv', 'w')
        csv.write('Input file name,Output file name,Max tree depth,Min node size,Min fill ratio,Min pixel opacity,# of nodes,# of leaf nodes,Image pixels,Tree pixels,False positives,False negatives,Total error\n')

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
                        quad_coll.drawTree(img2, tree, True)
                        draw = ImageDraw.Draw(img2)
                        draw.text((0, 0), 'max tree depth: %d' % d)
                        draw.text((0, 10), 'min node size: %d pixels' % s)
                        draw.text((0, 20), 'min node fill ratio: %f pixels' % r)
                        draw.text((0, 30), 'min filled pixel opactiy:%f alpha' % o)

                        outfilename = dirName + '/' + imgName + ('%04d' % n) + f[f.rfind('.'):]
                        ImageChops.composite(img2, img, img2).save(outfilename)
                        n = n + 1

                        error = quad_coll.calcError(img, tree)
                        csv.write('%s,%s,%d,%d,%f,%f,%d,%d,%d,%d,%d,%d,%d\n' % (\
                            f,\
                            outfilename,\
                            d,\
                            s,\
                            r,\
                            o,\
                            tree.getNumNodes(),\
                            tree.getNumLeafNodes(),\
                            error['imgPixels'],\
                            error['treePixels'],\
                            error['falsePositives'],\
                            error['falseNegatives'],\
                            error['falsePositives'] + error['falseNegatives']\
                        ))
        
        csv.close()