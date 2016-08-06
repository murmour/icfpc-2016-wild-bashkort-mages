
from icfp_api import *


if __name__ == '__main__':
    sol = parse_solution_fname(sys.argv[1])
    print(send_solution(sol['set_id'], sol['fname']))
