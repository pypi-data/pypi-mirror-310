#coding: utf-8
from setuptools import setup, find_packages

setup(
    name='m3_xlrd',
    version='0.9.4.2',
    url='https://stash.bars-open.ru/projects/M3/repos/m3-xlrd/browse',
    license='Apache License, Version 2.0',
    author='BARS Group',
    author_email='a.morozov@bars.group',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    description='Патч официальной библиотеки xlrd для работы с excel-файлами',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
