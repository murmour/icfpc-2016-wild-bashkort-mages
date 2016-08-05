
import subprocess
import codecs
import sys
import re
import io
import time
import json
from os import listdir


api_key = '149-9813263d3c764afad44eeebcb61a4cd8'


def api_get_request(url) -> str:
    res = subprocess.check_output(
        ['curl',
         '--compressed',
         '-L',
         '-H', 'Expect:',
         '-H', 'X-API-Key: %s' % api_key,
         url ])
    time.sleep(2)
    return res.decode('utf-8')


def send_solution(id) -> str:
    res = subprocess.check_output(
        ['curl',
         '--compressed',
         '-L',
         "-X", "POST",
         '-H', 'Expect:',
         '-H', 'X-API-Key: %s' % api_key,
         '-F', 'problem_id=%d' % id,
         '-F', 'solution_spec=@../data/solutions/%d.out' % id,
         'http://2016sv.icfpcontest.org/api/solution/submit' ])
    time.sleep(2)
    return json.loads(res.decode('utf-8'))


def get_hello() -> json:
    print('Hello, world...')
    res = api_get_request('http://2016sv.icfpcontest.org/api/hello')
    return json.loads(res)


def get_json_blob(hash) -> json:
    print('Getting blob %s...' % hash)
    res = api_get_request('http://2016sv.icfpcontest.org/api/blob/%s' % hash)
    return json.loads(res)


def get_blob(hash) -> json:
    print('Getting blob %s...' % hash)
    res = api_get_request('http://2016sv.icfpcontest.org/api/blob/%s' % hash)
    return res


def get_snapshot_list() -> json:
    print('Getting snapshot list...')
    res = api_get_request('http://2016sv.icfpcontest.org/api/snapshot/list')
    return json.loads(res)


def get_latest_snapshot() -> json:
    print('Getting latest snapshot...')
    l = get_snapshot_list()['snapshots'][-1]
    return get_json_blob(l['snapshot_hash'])


def get_latest_problems() -> json:
    print('Getting latest problems...')
    s = get_latest_snapshot()
    return s['problems']


def write_latest_problem_specs() -> json:
    print('Writing latest problem specs...')
    for p in get_latest_problems():
        spec = get_blob(p['problem_spec_hash'])
        fname = '../data/problems/%s.in' % p['problem_id']
        with open(fname, 'w') as f:
            f.write(spec)


if __name__ == '__main__':
    print(int(sys.argv[1]))
