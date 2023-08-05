import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='statsBotClient',
      version='0.1',
      description='Client of the bot for collecting statistics',
      url='https://github.com/MinaevaKsenia/statsBot',
      author='Minaeva Ksenia',
      author_email='minaeva.ksen@gmail.com',
      zip_safe=False,
      long_description=read('README.md'),
      packages=[],
      include_package_data=True,
      test_suite="tests"
      )
