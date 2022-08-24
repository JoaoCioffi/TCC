import os
import joblib

absPath = os.path.dirname(__file__)
relPath = "dependencies"
filesPath = os.path.join(absPath,relPath)

def findAnomaly(filename='anomalyDetector.joblib',path=filesPath):
    os.chdir(filesPath)
    classifierAlg = joblib.load(filename)
    os.chdir(absPath)
    return classifierAlg