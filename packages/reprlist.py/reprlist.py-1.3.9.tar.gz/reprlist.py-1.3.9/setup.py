# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 16:24:54 2020

@author: Ray
"""

from setuptools import setup, find_packages

with open('reprlist/README.rst') as rd:
    long_description = rd.read()
# with open('LICENSE') as fp:
#     license = fp.read()

setup(name='reprlist.py',
      version='1.3.9',
      py_modules=['Reprlist'],
      packages=find_packages(),
      package_data={'reprlist.py': ('globalrule.json',)},
      author='Juntong',
      author_email='jessica_ye2015@sina.com.cn',
      long_description=long_description,
      long_description_content_type="text/x-rst",
      license="MIT License",
      description='Create and edit multiline text(str), a tool to realize __repr__.',
      keywords='repr multiline str char text',
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent"],
      )

'''
    !python setup.py sdist bdist_wheel
    !twine upload dist/*
'''
