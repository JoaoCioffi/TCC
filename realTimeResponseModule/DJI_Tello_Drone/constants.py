import pandas as pd
import os

absPath = os.path.dirname(__file__)
relPath = "dependencies"
filesPath = os.path.join(absPath,relPath)

def loadStatistics(filename='fv_statistics.csv',path=filesPath):
    os.chdir(filesPath)
    statistics = pd.read_csv(filename)
    return statistics