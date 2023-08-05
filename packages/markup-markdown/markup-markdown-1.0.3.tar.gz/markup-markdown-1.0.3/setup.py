#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

from os import path
import shutil

# if path.isfile('README.md'):
#     shutil.copyfile('README.md', 'README')

setup(
    name='markup-markdown',
    description='Mark Markdown Up',
    version='1.0.3',
    author='John Reese, Hai Liang W.',
    author_email='hailiang.hl.wang@gmail.com',
    url='https://github.com/hailiang-wang/markdown-pp',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
        'Development Status :: 5 - Production/Stable',
    ],
    license='MIT License',
    packages=['markup', 'markup/Modules'],
    entry_points={
        'console_scripts': [
            'markup = markup.main:main'
        ],
    },
    install_requires=[
        'Watchdog >= 0.8.3',
    ],
)
