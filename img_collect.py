'''
main script
'''

import logging
import sys

from baidu.location2imgs import ImageCollector

LOGLEVEL = logging.WARN

try:
    # add -v to set loglevel to DEBUG
    if sys.argv[3] == "-v":
        LOGLEVEL = logging.DEBUG

    COLLECTOR = ImageCollector(sys.argv[1], sys.argv[2], LOGLEVEL)
    COLLECTOR.main()

except IndexError:
    print("usage:", sys.argv[0], "<query> <region> -v")
    sys.exit(1)
except KeyboardInterrupt:
    sys.exit(1)
