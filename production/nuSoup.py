# Extracting NUWorks from raw html files
# Justin Miller, Northeastern University COE
# Paxton Howard, Northeastern University COS

# Modules
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import sys
import os


# Getting all text files in data folder
filePath = sys.path[0][:-10] + "rawFiles/"
fileList = os.listdir(filePath)

# Function to soup
def soupFile(filePath,fileName):

    # Open File
    file = open(filePath + fileName, 'r')
    content = file.read()
    file.close()

    # Soup
    soup = BeautifulSoup(content)

    return soup

soup = soupFile(filePath,fileList[0])
