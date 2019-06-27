# coding: utf-8
import setuptools

import os

here = os.path.abspath(os.path.dirname(__file__))

info = {}

with open(os.path.join(here, 'TorPool', '__version__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), info)

packages = ['TorPool']

requires = [
    'flask>=1.0.2',
]

setuptools.setup(
    name=info['__title__'],
    version=info['__version__'],
    author=info['__author__'],
    author_email=info['__author_email__'],
    description=info['__description__'],
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url=info['__url__'],
    packages=packages,
    include_package_data=True,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*",
    packages_dir={'TorPool': 'TorPool',},
    package_data={
        '': ['LICENSE', ],
        'TorPool': ['TorPool'],
    },
    install_requires=requires,
    licence=info['__license__'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)