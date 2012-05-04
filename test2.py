from PIL import Image
from PIL import ImageDraw
from PIL import ImageChops
from os import listdir

import quad_coll

depths = [4, 8, 16]
sizes = [2, 4, 6, 8, 10]
ratios = [.01, .05, .1, .25]
opacities = [.1, .25, .5, .75, .9]

for f in listdir('.'):
    try:
        img = Image.open(f)
    except IOError:
        pass
    else:
        n = 0
        csv = file(f[:f.rfind('.')] + '_trees.csv', 'w')
        csv.write('Input file name,Output file name,Max tree depth,Min node size,Min fill ratio,Min pixel opacity,# of nodes,# of leaf nodes,Image pixels,Tree pixels,False positives,False Positives %,False negatives,False negatives %\n')

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

                        outfilename = f[:f.rfind('.')] + ('%04d' % n) + f[f.rfind('.'):]
                        ImageChops.composite(img2, img, img2).save(outfilename)
                        n = n + 1

                        error = quad_coll.calcError(img, tree)
                        csv.write('%s,%s,%d,%d,%f,%f,%d,%d,%d,%d,%d,%f,%d,%f\n' % (\
                            f,\
                            outfilename,\
                            d,\
                            s,\
                            r,\
                            o,\
                            tree.numNodes(True),\
                            tree.numNodes(False),\
                            error['imgPixels'],\
                            error['treePixels'],\
                            error['falsePositives'],\
                            error['falsePositives']/float(error['treePixels']),\
                            error['falseNegatives'],\
                            error['falseNegatives']/float(error['imgPixels']),\
                        ))

        
        csv.close()