#!/usr/bin/env python

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    author="Marc Heinrich",
    author_email='marc.heinrich@free.fr',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: MacOS', 
        'Operating System :: Microsoft :: Windows', 
        'Operating System :: POSIX', 
        'Topic :: Software Development :: Code Generators'
    ],
    description="Generate text document from simple scripts using your favorite language.",
    url="https://framagit.org/squirrrr/stupidgen",
    install_requires=[],
    entry_points={
        'console_scripts': ['stupidgen=stupidgen.__main__:main']
    },
    license="GNU General Public License v3",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='stupidgen',
    name='stupidgen',
    packages=['stupidgen'],
    package_dir = {'': 'src'},
    version='0.3.0', # Keep this value in sync with __init__.py
    provides = 'stupidgen'
)
