import os
import joblib

absPath = os.path.dirname(__file__)
relPath = "dependencies"
filesPath = os.path.join(absPath,relPath)

def loadBinaries(path=filesPath):

    os.chdir(filesPath)

    module1 = joblib.load('anomalyDetector.joblib')
    module2 = joblib.load('clusters.joblib')

    # flight statistics
    stats={
        'flightVariables':['roll','pitch','heading',
        'rollRate','pitchRate','yawRate','groundSpeed',
        'climbRate','altitudeRelative', 'throttlePct'],
        'Avg':[
            0.05329,-0.25034,157.156421,
            0.024987,0.212036,0.042293,
            3.158141,-0.0,14987,12.836437,68.796744
            ],
        'Std':[
              4.805201,8.521218,173.673083,
              7.385070,8.341805,10.646332,
              1.940292,0.418154,4.605824,11.678028
            ]
    }

    os.chdir(absPath)

    return module1,module2,stats