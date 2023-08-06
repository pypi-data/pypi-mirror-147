from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Portfolio standard deviation calculator'
long_description = 'This package allows you to compute the standard deviation of a portfolio, \n' \
                   'whatever it is the number of stocks are in it.\n' \
                    '------------------------------------------------------------------------------------------------------\n' \
                    'Arguments needed:\n' \
                    "-list of the stock's tickers\n" \
                    '-list of respective weights\n' \
                    '-starting year from when collect data\n' \
                    '-starting month from when collect data\n' \
                    'starting day from when collect data\n' \
                    '--------------------------------------\n' \
                    "The algorithm follow this formula and it's based on the returns of the stocks:\n" \
                                        "σ² = Σ°Σ'[w°w'σ(R°,R')]\n"


# Setting up
setup(
    name="Bruni",
    version=VERSION,
    author="Federico Bruni",
    author_email="brunifederico99@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pandas', 'pandas-datareader', 'numpy','datetime'],
    keywords=['python', 'portfolio', 'standard deviation', 'std', 'stocks','Bruni'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3.9",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: MacOS :: MacOS X"

    ]
)