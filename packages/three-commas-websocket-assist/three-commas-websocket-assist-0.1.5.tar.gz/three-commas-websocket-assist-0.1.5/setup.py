"""
PIP setup file
"""

from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='three-commas-websocket-assist',
    packages=['three_commas_websocket_assist'],
    version='0.1.5',
    description='3commas websocket stream assist',
    url='https://github.com/badass-blockchain/python-three-commas',
    author='Ron Klinkien & Ian Hogers',
    author_email='info@ianhogers.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'': 'src'},
    keywords=['python', '3commas', 'api', 'crypto', 'cryptocurrency',
              'three commas', 'bitcoin', 'trading', 'btc', 'eth', 'websocket'],
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    install_requires=['rel==0.4.7', 'websocket-client==1.3.2'],
    dependency_links=[]
)
