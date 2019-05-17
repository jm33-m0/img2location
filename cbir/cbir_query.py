'''
takes an input img, query the whole img database using selected method
'''

from __future__ import print_function

import logging
import os

from cbir.DB import Database
from cbir.edge import Edge
from cbir.evaluate import infer
from cbir.HOG import HOG
from cbir.resnet import ResNetFeat
from cbir.vggnet import VGGNetFeat


class CbirQuery:
    '''
    takes an input img from ./query/query_class/img.jpg,
    query the whole img database using selected method
    '''

    def __init__(self, method, verbose=False):
        self.verbose = verbose
        self.method = method
        self.depth = 5
        self.d_type = 'd1'

        if verbose:
            logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                                datefmt='%Y-%m-%d %I:%M:%S %p',
                                level=logging.DEBUG,
                                filename="./query.log")

        # methods to use
        self.methods = {
            "edge": Edge,
            "hog": HOG,
            "vgg": VGGNetFeat,
            "resnet": ResNetFeat
        }

    def get_query_img(self):
        '''
        feed img data to database
        '''
        query_db = Database("query", "query.csv")
        query_sample = getattr(
            self.methods[self.method](), "make_samples")(query_db)

        logging.debug("\n\n[*] query_db data: %s\n[*] query_sample: %s\n\n",
                      query_db.get_data(), query_sample)

        return query_sample[0]

    def query(self):
        '''
        query_img: path to input img
        '''
        # query the first img in query.csv
        query = self.get_query_img()
        os.system("rm cache -rf")

        # img db to search in
        img_db = Database("database", "database.csv")

        # call make_samples(db) accordingly
        samples = getattr(self.methods[self.method](), "make_samples")(img_db)
        logging.debug("SAMPLES: %s", samples)

        _, result = infer(query, samples=samples,
                          depth=self.depth, d_type=self.d_type)

        if self.verbose:
            print("\n[+] query: {}\n".format(query["img"]))

            for match in result:
                print("{}:\t{},\tClass {}".format(match["img"],
                                                  match["dis"],
                                                  match["cls"]))
