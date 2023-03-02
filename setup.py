from setuptools import setup, find_packages
try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()
VERSION = '0.0.53'
DESCRIPTION = 'A library used to simulate photovoltaic energy production using PVGIS'
# Setting up
setup(
    name="pvmodule",
    version=VERSION,
    author="Fábio Almeida",
    author_email="<fabio-r-almeida@outlook.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests', 'pandas', 'tzwhere','geopy','numpy','tabulate','datetime'],
    keywords=['Python', 'PVGIS', 'Simulator', 'Photovoltaic', 'Solar energy', 'Solar panels','Solar simulation'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
