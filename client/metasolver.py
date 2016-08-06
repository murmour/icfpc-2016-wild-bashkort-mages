
import icfp_api
import sys
import io


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('Usage: metasolver.py executable tag lowIndex highIndex ?iterations')
        sys.exit(1)

    executable = sys.argv[1]
    tag = sys.argv[2]

    problems = icfp_api.filter_problems(int(sys.argv[3]), int(sys.argv[4]))
    for p in problems:
        if len(sys.argv) < 6:
            sol = icfp_api.solve_problem(executable, p)
        else:
            iters = sys.argv[5]
            sol = icfp_api.solve_problem(executable, p, iters)
        if sol != None:
            sol_file = '../data/solutions/solution_%d_%s.out' % (p['id'], tag)
            with io.open(sol_file, 'w') as h:
                h.write(sol)
