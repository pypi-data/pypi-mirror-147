#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: caizhongming
# Mail: zhongming.cai@foxmail.com
# Created Time:  2021-1-13 21:17:34
#############################################


from setuptools import setup, find_packages

setup(
    name="pdemo",
    version="0.1.0",
    keywords=("pip", "pathtool","timetool", "magetool", "mage"),
    description="pip demo",
    long_description="pip demo!!!",
    license="MIT Licence",

    url="https://github.com/ezhonca/pdemo.git",
    author="caizhongming",
    author_email="zhongming.cai@foxmail.com",

    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "pdemo=pdemo.__main__:main"
        ],
    },
    include_package_data=True,
    platforms="any",
    install_requires=[]
)