# read the contents of your README file
from os import path

from setuptools import setup

INSTALL_REQUIRES = [
    'requests>=2.25.1',
    'plogger>=1.0.6'
]

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tcclient',
    version='0.0.4',
    packages=['tcclient'],
    url='https://github.com/c-pher/tcclient',
    license='GNU General Public License v3.0',
    author='Andrey Komissarov',
    author_email='a.komisssarov@gmail.com',
    description='The cross-platform tool to with the TC server remotely.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    install_requires=INSTALL_REQUIRES,
    python_requires='>=3.6',
)
