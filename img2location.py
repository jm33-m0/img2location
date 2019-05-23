'''
main script
'''

import argparse
import logging
import os
import sys

from cbir.cbir_query import CbirQuery
from imgcollector.location2imgs import ImageCollector


def get_args():
    '''
    takes care of args
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query", help="Query string for baidu map")
    parser.add_argument("-r", "--region", help="Query region for baidu map")
    parser.add_argument("-v", "--verbose",
                        help="Increase output verbosity", action="store_true")
    parser.add_argument("-c", "--cbironly",
                        help="Do not download new images from baidu map", action="store_true")

    return parser.parse_args()


def main():
    '''
    we need a fucking main
    '''
    loglevel = logging.WARN
    verbose = False

    args = get_args()
    if args.verbose:
        loglevel = logging.DEBUG
        verbose = True

    if args.cbironly:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                            datefmt='%Y-%m-%d %I:%M:%S %p',
                            level=loglevel,
                            filename="./img2location.log")
    else:
        collector = ImageCollector(args.query, args.region, loglevel)
        print("[*] Requesting images from baidu map...")
        collector.main()

    query = CbirQuery("resnet", verbose=verbose)
    print("[*] CBIR working...")
    result = query.query()

    # deal with CBIR result
    for match in result:
        addr = match['img'].split('---')[1].split('.')[0]
        diff = match['dis']

        print("\nMatching address:\n{}: {}".format(diff, addr))

    os.system("rm -f *.csv")


try:
    main()
except KeyboardInterrupt:
    print("Exiting...")
    sys.exit(1)
