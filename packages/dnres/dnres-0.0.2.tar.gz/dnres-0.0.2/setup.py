from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Managing and sharing data and results of analysis.'
LONG_DESCRIPTION = 'A package that facilitates modular type of data analysis providing a framework for managing generated data and resuls.'

# Setting up
setup(
    name="dnres",
    version=VERSION,
    author="Dimitrios Kioroglou",
    author_email="<d.kioroglou@hotmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['rich'],
    keywords=['python', 'data analysis', 'bioinformatics', 'reporting', 'analysis results'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
