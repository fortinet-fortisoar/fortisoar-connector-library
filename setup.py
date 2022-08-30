""" Copyright start
  Copyright (C) 2008 - 2022 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """

from setuptools import find_packages, setup

setup(
    name='fortisoar-connector-engine',
    packages=find_packages(include=['connectors', 'connectors.core', 'connectors.scripts', 'integrations']),
    version='1.0.0',
    description='FortiSOAR Connector Engine Library',
    author='Fortinet',
    license='MIT',
)
