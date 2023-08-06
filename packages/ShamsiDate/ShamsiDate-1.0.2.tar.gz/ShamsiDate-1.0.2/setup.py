#!/usr/bin/env python
import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

VERSION = '1.0.2'

setup(name='ShamsiDate',
      version=VERSION,
      description="Convert Shamsi to Gregorian date and vice versa",
      long_description=README,
      author='Samic',
      author_email='shamsi@samic.org',
      url='https://gitlab.com/samic130/shamsi/',
      license='GPLv3',
      packages=["shamsidate"],
      classifiers =[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",],
      include_package_data=True,
      zip_safe=False,
      entry_points={'console_scripts': [
          'shamsi = shamsidate.shamsi:main',]})
