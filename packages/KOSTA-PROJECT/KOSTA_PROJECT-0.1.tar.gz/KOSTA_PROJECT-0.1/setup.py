from distutils.core import setup

from setuptools import find_packages


setup(
  name = 'KOSTA_PROJECT',
  packages = find_packages(),
  version = '0.1',
  license='MIT',
  description = 'Test project',
  author = 'Kanstantsin Salanovich',
  author_email = 'solonovichyoo@gmail.com',
  url = 'https://github.com/kostaaaaa/tms_studing',
  keywords = ['TEST'],
  install_requires=[
          'numpy==1.22.3',
      ],
)