#!/usr/bin/env python
import os
from setuptools import setup


def _read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


REQUIREMENTS = [l for l in _read('requirements.txt').split('\n') if l and not l.startswith('#')]
VERSION = '0.1.0'

setup(
        name='bottle-tinyrpc',
        version=VERSION,
        url='https://github.com/cope-systems/bottle-tinyrpc',
        #download_url='https://github.com/cope-systems/bottle-tinyrpc/archive/v{}.tar.gz'.format(VERSION),
        description='TinyRPC Integration for the Bottle Web Framework',
        long_description=_read("README.md"),
        author='Robert Cope',
        author_email='robert@copesystems.com',
        license='MIT',
        platforms='any',
        packages=["bottle_tinyrpc"],
        install_requires=REQUIREMENTS,
        tests_require=REQUIREMENTS + ["pytest", "webtest"],
        classifiers=[
            'Environment :: Web Environment',
            'Environment :: Plugins',
            'Framework :: Bottle',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'Topic :: Software Development :: Libraries :: Python Modules'
        ],
        include_package_data=True
)
