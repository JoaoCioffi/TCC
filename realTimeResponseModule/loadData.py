import pandas as pd
import os

absPath = os.path.dirname(__file__)
relPath = "dependencies"
filesPath = os.path.join(absPath,relPath)

def loadData(filename='rawData.csv',path=filesPath):
    os.chdir(filesPath)
    data = pd.read_csv(filename,sep=";")
    return data