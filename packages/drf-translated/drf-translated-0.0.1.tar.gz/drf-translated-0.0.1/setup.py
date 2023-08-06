import os
import codecs
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'

DESCRIPTION = 'DRF modeltranslation serializer'

# Setting up
setup(
    name="drf-translated",
    version=VERSION,
    author="Kapustlo",
    description=DESCRIPTION,
    url='https://notabug.org/kapustlo/drf-translated',
    long_description_content_type="text/markdown",
    long_description=long_description,
    package_dir={'': 'drf_translated'},
    packages=find_packages(where='drf_translated'),
    keywords=['python', 'python3', 'modeltranslation', 'drf', 'serializer'],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Internet :: WWW/HTTP",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[ 
        'django',
        'djangorestframework',
        'django-modeltranslation'
    ]
)
