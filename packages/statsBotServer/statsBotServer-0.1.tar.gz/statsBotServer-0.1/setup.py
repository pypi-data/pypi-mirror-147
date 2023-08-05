import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='statsBotServer',
      version='0.1',
      description='Server of the bot for collecting statistics',
      url='https://github.com/MinaevaKsenia/statsBot',
      author='Minaeva Ksenia',
      author_email='minaeva.ksen@gmail.com',
      zip_safe=False,
      packages=['src', 'src/utils', 'src/views'],
      long_description=read('README.md'),
      include_package_data=True,
      test_suite="tests"
      )
