#!/usr/bin/env python

import os
import sys
from setuptools import setup
os.listdir

setup(
   name='ix2_56x',
   version='1.0',
   description='Module to initialize Quanta IX2-56X platforms',
   
   packages=['ix2_56x'],
   package_dir={'ix2_56x': 'ix2-56x/classes'},
)

