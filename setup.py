from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'A library used to simulate photovoltaic energy production using PVGIS'
LONG_DESCRIPTION = 'A package that allows to build systems and simulate energy production using real-world data from PVGIS.'

# Setting up
setup(
    name="pv-sim",
    version=VERSION,
    author="Fábio Almeida",
    author_email="<fabio-r-almeida@outlook.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests', 'pandas', 'tzwhere','geopy','numpy','warnings'],
    keywords=['python', 'PVGIS', 'simulator', 'photovoltaic', 'solar energy', 'solar panels','solar simulation'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)