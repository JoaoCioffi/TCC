import numpy as np
import pandas as pd
import os

absPath = os.path.dirname(__file__)
relPath = "dependencies"
filesPath = os.path.join(absPath,relPath)

def oneCosineGust(filename='rawData.csv',path=filesPath):
    os.chdir(filesPath)
    data = pd.read_csv(filename,sep=";")[['roll','pitch','heading','rollRate',
                                          'pitchRate','yawRate','groundSpeed',
                                          'climbRate','altitudeRelative','throttlePct']] # we must NEVER change this! 
                                                                                         # (those were the models' dependencies during the previous fitting steps)
    
    time = [] # time to be appended (in seconds)
    for t in range(0,len(data)):
        time.append(t)
        
    data['time'] = time

    return time

print(oneCosineGust())