from setuptools import setup
from ServerTime import __version__

setup(
    name='ServerTime',
    version=__version__,
    description='Get server time from http | https URLs.',
    long_description='# Usage:\n```shell\npython -m ServerTime.CLI https://www.google.com\n```',
    long_description_content_type='text/markdown',
    author='LUA9',
    maintainer='LUA9',
    packages=['ServerTime']
)