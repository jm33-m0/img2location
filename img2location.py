'''
main script
'''

import sys

from cbir.cbir_query import CbirQuery


def main():
    '''
    run me
    '''
    query = CbirQuery("resnet", verbose=True)
    query.query()


try:
    main()
except KeyboardInterrupt:
    sys.exit(1)
