# pylint: disable=invalid-name,missing-docstring,exec-used,too-many-arguments,too-few-public-methods,no-self-use
from __future__ import print_function

import sys
from cbir.color import Color
from cbir.daisy import Daisy
from cbir.DB import Database
from cbir.edge import Edge
from cbir.evaluate import infer
from cbir.gabor import Gabor
from cbir.HOG import HOG
from cbir.resnet import ResNetFeat
from cbir.vggnet import VGGNetFeat

depth = 5
d_type = 'd1'
query_idx = 0

if __name__ == '__main__':
    db = Database()

    # methods to use
    methods = {
        "color": Color,
        "daisy": Daisy,
        "edge": Edge,
        "hog": HOG,
        "gabor": Gabor,
        "vgg": VGGNetFeat,
        "resnet": ResNetFeat
    }

    try:
        mthd = sys.argv[1].lower()
    except IndexError:
        print("usage: {} <method>".format(sys.argv[0]))
        print("supported methods:\ncolor, daisy, edge, gabor, hog, vgg, resnet")

        sys.exit(1)

    # call make_samples(db) accordingly
    samples = getattr(methods[mthd](), "make_samples")(db)

    # query the first img in data.csv
    query = samples[query_idx]
    print("\n[+] query: {}\n".format(query["img"]))

    _, result = infer(query, samples=samples, depth=depth, d_type=d_type)

    for match in result:
        print("{}:\t{},\tClass {}".format(match["img"],
                                          match["dis"],
                                          match["cls"]))
