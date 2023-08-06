# Introduction
This package contains utilities used to extend robot capabilities through python.

# Build DeltekLib
Steps in creating distributable python library
1. CD: DeltekLib parent folder
2. PS: python setup.py bdist_wheel
3. Copy generated wheel (.whl) file from dist folder to repository

# Usage
Steps in using DeltekLib
1. From the test machine, download the wheel file from the repository
2. Run "pip install [download_folder]\DeltekLib-1.0.0-py3-none-any.whl" (make sure to use the correct version from the repository)
3. Open a robot file and include the needed Library

    *** Settings ***
    
    Library  WinRM

# Contribute
Feel free to add in python libraries that will be useful in test automation.
