# setup.py
from setuptools import setup, find_packages

setup(
    name="datacleaners",
    version="0.4.0",
    author="Nagesh",
    author_email="nageshmashette32@gmail.com",
    description="A package for cleaning data before machine learning.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/NageshMashette/dataCleaner",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn"
    ],
)
