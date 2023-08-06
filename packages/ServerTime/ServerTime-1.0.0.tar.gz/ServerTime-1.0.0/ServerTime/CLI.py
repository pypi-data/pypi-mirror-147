import time
from sys import exit
from argparse import ArgumentParser

from . import GetServerTime

if __name__ != '__main__':
    raise ImportError('ServerTime.CLI is not available for import.')

parser = ArgumentParser()
parser.add_argument('URL', type=str)

arguments = parser.parse_args()

try:
    while True:
        result = GetServerTime(arguments.URL)
        print('\033[H\033[J' + result)
        time.sleep(1)
except KeyboardInterrupt:
    exit(1)