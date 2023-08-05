#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='bawx-player',
    version='0.9.1',
    description='Karaoke player library (and more)',
    long_description= open('../README.md', 'r').read(),
    long_description_content_type="text/markdown",
    author='Michael Ottoson',
    author_email='michael@pointw.com',
    url='https://github.com/pointw-dev/bawx-player',
    keywords=['karaoke'],
    packages=['bawx_player'],
    license='MIT',
    install_requires=['numpy>=1.22.3', 'pygame>=2.1.2'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers'
    ]
)
