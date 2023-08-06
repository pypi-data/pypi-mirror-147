from setuptools import setup, find_packages
import sys
import os

setup(
    name="nonebot_plugin_dida",
    version="1.0.0",
    author="TDK",
    author_email="tdk1969@foxmail.com",
    description="基于Nonebot的滴答清单插件,可创建普通任务/子任务,按照条件查询任务",
    long_description=open("README.rst", "r").read(),
    include_package_data=True,
    license="GNU",
    url="https://github.com/TDK1969/nonebot_plugin_dida",
    packages=['nonebot_plugin_dida'],
    install_requires=[
        "requests",
        "nonebot_plugin_apscheduler",
    ],
    keywords='nonebot',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],

)