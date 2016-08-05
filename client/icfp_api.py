
import subprocess
import codecs
import sys
import re
import io
import time
import json
from os import listdir


api_key = '149-9813263d3c764afad44eeebcb61a4cd8'


def get_hello() -> bool:
    print('Hello, world...')
    response = subprocess.check_output(
        ['curl',
         '--compressed',
         '-L',
         '-H', 'Expect:',
         '-H', 'X-API-Key: %s' % api_key,
         'http://2016sv.icfpcontest.org/api/hello' ])
    return json.loads(response.decode('utf-8'))


if __name__ == '__main__':
    print(get_hello())
