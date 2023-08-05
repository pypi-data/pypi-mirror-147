#!/usr/bin/env python
#-*- coding:utf-8 -*-
 
#############################################
# File Name: setup.py
# Author: cikuu
# Mail: info@cikuu.com
# Created Time: 2022-2-13
#############################################
 
from setuptools import setup, find_packages
 
setup(
  name = "cikuu",
  version = "2022.4.18",
  keywords = ("pip"),
  description = "cikuu tools",
  long_description = "cikuu tools, commonly used, spacy3.1.1",
  license = "MIT Licence",
 
  url = "http://www.cikuu.com",
  author = "cikuu",
  author_email = "info@cikuu.com",
 
  packages = find_packages(),
  include_package_data = True,
  platforms = "any", #"pymysql","pika","fastapi","uvicorn",
  install_requires = ["fire","redis","elasticsearch","marisa_trie","click==7.1.2","requests"]  #>=2.27.1
)
