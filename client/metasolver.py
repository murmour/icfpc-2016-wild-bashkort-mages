
from icfp_api import *
import sys
import io


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('Usage: metasolver.py executable tag lowIndex highIndex ?iterations')
        sys.exit(1)

    executable = sys.argv[1]
    tag = sys.argv[2]

    problems = filter_problems(int(sys.argv[3]), int(sys.argv[4]))
    for p in problems:
        if ensure_that_problem_is_unsolved(p['id']):
            sol_file = '../data/solutions/solution_%d_%s.out' % (p['id'], tag)
            if os.path.isfile(sol_file):
                print('Solution file for problem %d already exists.' % p['id'])
            else:
                if len(sys.argv) < 6:
                    sol = solve_problem(executable, p)
                else:
                    iters = sys.argv[5]
                    sol = solve_problem(executable, p, iters)
                if sol != None:
                    with io.open(sol_file, 'w') as h:
                        h.write(sol)
