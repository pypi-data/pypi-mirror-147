#! /usr/bin/env python

"""Genetic Programming in Python, with a scikit-learn inspired API. Generating corresponding rule formula from given Cellular Automaton."""

from setuptools import setup, find_packages
import CAlearn

DESCRIPTION = __doc__
VERSION = CAlearn.__version__

setup(name='CAlearn',
      version=VERSION,
      description=DESCRIPTION,
      long_description=open("README.rst").read(),
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved',
                   'Topic :: Software Development',
                   'Topic :: Scientific/Engineering',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: Unix',
                   'Operating System :: MacOS',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8'],
      author='Chen Shu',
      author_email='shuchen.math@gmail.com',
      url='https://github.com/ChenShuMath/CAlearn',
      license='new BSD',
      packages=find_packages(exclude=['*.tests',
                                      '*.tests.*']),
      zip_safe=False,
      package_data={'': ['LICENSE']},
      install_requires=['scikit-learn>=0.22.1',
                        'joblib>=0.13.0'])