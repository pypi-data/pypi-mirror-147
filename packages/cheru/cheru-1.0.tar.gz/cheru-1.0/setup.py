from distutils.command.install_scripts import install_scripts
from setuptools import setup
setup(name="cheru",
version="1.0",
description="This pakage helps the user to download reviews from amazon and flipkart . created by chetan",
long_description="This pakage was created by chetan for any more quries please contact me, 8792381530",
author="Chetan",
packages=["cheru"],
install_requires=[
        "pandas",
        "numpy",
        "requests",
        "textblob",
        "bs4",
        "matplotlib",
        "nltk",
        
        "seaborn"   
    ] )