#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：max_pkg 
@File    ：setup.py
@IDE     ：PyCharm 
@Author  ：maxluuu@126.com
@Date    ：2024/11/25 20:25 
@Brief   ：
"""

import setuptools  # 导入setuptools打包工具

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="max_pkg",  # 用自己的名替换其中的YOUR_USERNAME_
    version="0.0.1",  # 包版本号，便于维护版本
    author="maxluuu",  # 作者，可以写自己的姓名
    author_email="maxluuu@126.com",  # 作者联系方式，可写自己的邮箱地址
    description="A small package for eeg process",  # 包的简述
    long_description=long_description,  # 包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    url="https://gitcode.com/LuPIGGY/max_pkg/tree/main/max_pkg",  # 自己项目地址，比如github的项目地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',  # 对python的最低版本要求
)
