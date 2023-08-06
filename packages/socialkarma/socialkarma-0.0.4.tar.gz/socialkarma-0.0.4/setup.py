#!/usr/bin/env python

import setuptools

setuptools.setup(
      name='socialkarma', # This is the name of the package
      version='0.0.4',
      description='Social Karma Python SDK',
      author='Christopher Dang',               # Full name of the author
      author_email='chris@socialkarma.info',
      url='https://www.github.com/cdang1234/social-karma-python-sdk',
      packages=setuptools.find_packages(),    # List of all python modules to be installed
      python_requires='>=3.6',                # Minimum version requirement of the package
      py_modules=['socialkarma'],
      package_dir={'':'socialkarma/src'},     # Directory of the source code of the package
      install_requires=[]                     # Install other dependencies if any
)
