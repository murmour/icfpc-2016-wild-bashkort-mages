
from icfp_api import *


if __name__ == '__main__':
    print(send_problem(1470448800 + int(sys.argv[1]) * 3600, sys.argv[2]))
