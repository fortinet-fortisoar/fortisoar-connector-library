""" Copyright start
  MIT License
  Copyright (c) 2024 Fortinet Inc
  Copyright end """

from setuptools import find_packages, setup
import os

build_num = os.environ.get("i_build_number", 1)

release_verion=os.environ.get("release_version")

s_name=os.environ.get("s_wheel_pkg_name")

setup(
    name=f'{s_name}',
    packages=find_packages(include=['connectors', 'connectors.core', 'connectors.cyops_utilities', 'connectors.scripts', 'integrations']),
    version=f'{release_verion}-{build_num}',
    description='FortiSOAR Connector Engine Library',
    author='Fortinet',
    url='https://github.com/fortinet-fortisoar/fortisoar-connector-engine',
    license='MIT',
    install_requires=["requests", "markdown2", "pytest", "json2html", "camelcase", "Pillow"],
    package_data={'connectors.scripts': ['config/*', ]}
)
