from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="kms_dl_module",  
    version="0.1.0",       
    author="KMS",
    author_email="kms994438@gmail.com",
    description="A package for deep learning models including time series forecasting, classification, and text classification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(), 
    install_requires=[

        "keras",
        "matplotlib",
        "nltk",
        "numpy",
        "pandas",
        "scikit_learn",
        "seaborn",
        "setuptools",
        "setuptools",
        "tensorflow",
        "tensorflow_intel",

    ],  # List of dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.3",  # Minimum Python version requirement
)
