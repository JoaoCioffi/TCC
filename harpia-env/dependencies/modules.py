import os
import joblib
import numpy as np
import pandas as pd
import statistics as st

class API():
    
    def __init__(self):
        super(API,self).__init__()

    @classmethod
    def model(self,
              filesNamesList=['anomalyDetector.joblib',
                              'clusters.joblib']):
        absPath=os.path.dirname(__file__)
        relPath="joblib"
        filesPath=os.path.join(absPath,relPath)
        os.chdir(filesPath)
        stage_1=joblib.load(filesNamesList[0])
        stage_2=joblib.load(filesNamesList[1])
        loadedModel=[stage_1,stage_2]
        os.chdir(absPath)
        return loadedModel
    
    @classmethod
    def architecture(self,inputData):
        """
        >> Data sequence
        input array: roll,pitch,heading,rollRate,pitchRate,yawRate,groundSpeed,climbRate,altitudeRelative,throttlePct
        """
        loadedModel=self.model()
        statistics={
            'flightVariables':['roll','pitch','heading','rollRate','pitchRate','yawRate','groundSpeed','climbRate','altitudeRelative','throttlePct'],
            'avg':[0.053290,-0.250340,157.156421,0.024987,0.212036,0.042293,3.158141,-0.014987,12.836437,68.796744],
            'std':[4.805201,8.521218,173.673083,7.385070,8.341805,10.646332,1.940292,0.418154,4.605824,11.678028]
        }
        iterator=0
        for r in range(inputData.shape[0]):
            if loadedModel[0].predict(np.array([inputData[r][3:6]]))[0] == 1:
                iterator+=1
                if iterator>=5:
                    iterator=0
                    sequential = {'roll':[],
                          'pitch':[],
                          'heading':[],
                          'rollRate':[],
                          'pitchRate':[],
                          'yawRate':[],
                          'groundSpeed':[],
                          'climbRate':[],
                          'altitudeRelative':[],
                          'throttlePct':[]}
                    weightedCluster = []

                    #------------#
                    ## 0.roll:
                    rollAvg = statistics['avg'][0];rollStd = statistics['std'][0] #mean() and std()
                    upperBoundary_roll = rollAvg + 3*rollStd;lowerBoundary_roll = rollAvg - 3*rollStd #boundaries: mean() +/- 3std()
                    if lowerBoundary_roll <= inputData[r][0] <= upperBoundary_roll:
                        sequential['roll'].append('ok') #normal range (level=0)
                    elif (lowerBoundary_roll-rollStd) <= inputData[r][0] < lowerBoundary_roll or upperBoundary_roll < inputData[r][0] <= (upperBoundary_roll + rollStd):
                        sequential['roll'].append('mild') #over normal boundaries limited by 1std (level=1)
                    elif (lowerBoundary_roll-2*rollStd) <= inputData[r][0] < (lowerBoundary_roll-rollStd) or (upperBoundary_roll + rollStd) < inputData[r][0] <= (upperBoundary_roll+2*rollStd):
                        sequential['roll'].append('moderate') #between 1std and 2std (level=2)
                    else:
                        sequential['roll'].append('critical') #greater than 2std (level=3)
                    
                    #------------#
                    ## 1.pitch:
                    pitchAvg = statistics['avg'][1];pitchStd = statistics['std'][1]
                    upperBoundary_pitch = pitchAvg + 3*pitchStd;lowerBoundary_pitch = pitchAvg - 3*pitchStd
                    if lowerBoundary_pitch <= inputData[r][1] <= upperBoundary_pitch:
                        sequential['pitch'].append('ok')
                    elif (lowerBoundary_pitch-pitchStd) <= inputData[r][1] < lowerBoundary_pitch or upperBoundary_pitch < inputData[r][1] <= (upperBoundary_pitch + pitchStd):
                        sequential['pitch'].append('mild')
                    elif (lowerBoundary_pitch-2*pitchStd) <= inputData[r][1] < (lowerBoundary_pitch-pitchStd) or (upperBoundary_pitch + pitchStd) < inputData[r][1] <= (upperBoundary_pitch+2*pitchStd):
                        sequential['pitch'].append('moderate')
                    else:
                        sequential['pitch'].append('critical')
                    
                    #------------#
                    ## 2.heading:
                    headingAvg = statistics['avg'][2];headingStd = statistics['std'][2]
                    upperBoundary_heading = headingAvg + 3*headingStd;lowerBoundary_heading = headingAvg - 3*headingStd
                    if lowerBoundary_heading <= inputData[r][2] <= upperBoundary_heading:
                        sequential['heading'].append('ok')
                    elif (lowerBoundary_heading-headingStd) <= inputData[r][2] < lowerBoundary_heading or upperBoundary_heading < inputData[r][2] <= (upperBoundary_heading + headingStd):
                        sequential['heading'].append('mild')
                    elif (lowerBoundary_heading-2*headingStd) <= inputData[r][2] < (lowerBoundary_heading-headingStd) or (upperBoundary_pitch + headingStd) < inputData[r][2] <= (upperBoundary_heading+2*headingStd):
                        sequential['heading'].append('moderate')
                    else:
                        sequential['heading'].append('critical')
                    
                    #------------#
                    ## 3.rollRate:
                    rollRateAvg = statistics['avg'][3];rollRateStd = statistics['std'][3]
                    upperBoundary_rollRate = rollRateAvg + 3*rollRateStd;lowerBoundary_rollRate = rollRateAvg - 3*rollRateStd
                    if lowerBoundary_rollRate <= inputData[r][3] <= upperBoundary_rollRate:
                        sequential['rollRate'].append('ok')
                    elif (lowerBoundary_rollRate-rollRateStd) <= inputData[r][3] < lowerBoundary_rollRate or upperBoundary_rollRate < inputData[r][3] <= (upperBoundary_rollRate + rollRateStd):
                        sequential['rollRate'].append('mild')
                    elif (lowerBoundary_rollRate-2*rollRateStd) <= inputData[r][3] < (lowerBoundary_rollRate-rollRateStd) or (upperBoundary_rollRate + rollRateStd) < inputData[r][3] <= (upperBoundary_rollRate+2*rollRateStd):
                        sequential['rollRate'].append('moderate')
                    else:
                        sequential['rollRate'].append('critical')
                    #------------#
                    ## 4.pitchRate
                    pitchRateAvg = statistics['avg'][4];pitchRateStd = statistics['std'][4]
                    upperBoundary_pitchRate = pitchRateAvg + 3*pitchRateStd;lowerBoundary_pitchRate = pitchRateAvg - 3*pitchRateStd
                    if lowerBoundary_pitchRate <= inputData[r][4] <= upperBoundary_pitchRate:
                        sequential['pitchRate'].append('ok')
                    elif (lowerBoundary_pitchRate-pitchRateStd) <= inputData[r][4] < lowerBoundary_pitchRate or upperBoundary_pitchRate < inputData[r][4] <= (upperBoundary_pitchRate + pitchRateStd):
                        sequential['pitchRate'].append('mild')
                    elif (lowerBoundary_pitchRate-2*pitchRateStd) <= inputData[r][4] < (lowerBoundary_pitchRate-pitchRateStd) or (upperBoundary_pitchRate + pitchRateStd) < inputData[r][4] <= (upperBoundary_pitchRate+2*pitchRateStd):
                        sequential['pitchRate'].append('moderate')
                    else:
                        sequential['pitchRate'].append('critical')
                    
                    #------------#
                    ## 5.yawRate:
                    yawRateAvg = statistics['avg'][5];yawRateStd = statistics['std'][5]
                    upperBoundary_yawRate = yawRateAvg + 3*yawRateStd;lowerBoundary_yawRate = yawRateAvg - 3*yawRateStd
                    if lowerBoundary_yawRate <= inputData[r][5] <= upperBoundary_yawRate:
                        sequential['yawRate'].append('ok')
                    elif (lowerBoundary_yawRate-yawRateAvg) <= inputData[r][5] < lowerBoundary_yawRate or upperBoundary_yawRate < inputData[r][5] <= (upperBoundary_yawRate + yawRateAvg):
                        sequential['yawRate'].append('mild')
                    elif (lowerBoundary_yawRate-2*yawRateStd) <= inputData[r][5] < (lowerBoundary_yawRate-yawRateStd) or (upperBoundary_yawRate + yawRateStd) < inputData[r][5] <= (upperBoundary_yawRate+2*yawRateStd):
                        sequential['yawRate'].append('moderate')
                    else:
                        sequential['yawRate'].append('critical')
                    
                    #------------#
                    ## 6.groundSpeed:
                    groundSpeedAvg = statistics['avg'][6];groundSpeedStd = statistics['std'][6]
                    upperBoundary_groundSpeed = groundSpeedAvg + 3*groundSpeedStd;lowerBoundary_groundSpeed = groundSpeedAvg - 3*groundSpeedStd
                    if lowerBoundary_groundSpeed <= inputData[r][6] <= upperBoundary_groundSpeed:
                        sequential['groundSpeed'].append('ok')
                    elif (lowerBoundary_groundSpeed-groundSpeedAvg) <= inputData[r][6] < lowerBoundary_groundSpeed or upperBoundary_groundSpeed < inputData[r][6] <= (upperBoundary_groundSpeed + groundSpeedAvg):
                        sequential['groundSpeed'].append('mild')
                    elif (lowerBoundary_groundSpeed-2*groundSpeedStd) <= inputData[r][6] < (lowerBoundary_groundSpeed-groundSpeedStd) or (upperBoundary_groundSpeed + groundSpeedStd) < inputData[r][6] <= (upperBoundary_groundSpeed+2*groundSpeedStd):
                        sequential['groundSpeed'].append('moderate')
                    else:
                        sequential['groundSpeed'].append('critical')
                    #------------#
                    ## 7.climbRate
                    climbRateAvg = statistics['avg'][7];climbRateStd = statistics['std'][7]
                    upperBoundary_climbRate = climbRateAvg + 3*climbRateStd;lowerBoundary_climbRate = climbRateAvg - 3*climbRateStd
                    if lowerBoundary_climbRate <= inputData[r][7] <= upperBoundary_climbRate:
                        sequential['climbRate'].append('ok')
                    elif (lowerBoundary_climbRate-climbRateAvg) <= inputData[r][7] < lowerBoundary_climbRate or upperBoundary_climbRate < inputData[r][7] <= (upperBoundary_climbRate + climbRateAvg):
                        sequential['climbRate'].append('mild')
                    elif (lowerBoundary_climbRate-2*climbRateStd) <= inputData[r][7] < (lowerBoundary_climbRate-climbRateStd) or (upperBoundary_climbRate + climbRateStd) < inputData[r][7] <= (upperBoundary_climbRate+2*climbRateStd):
                        sequential['climbRate'].append('moderate')
                    else:
                        sequential['climbRate'].append('critical')
                    
                    #------------#
                    ## 8.altitudeRelative:
                    altitudeRelativeAvg = statistics['avg'][8];altitudeRelativeStd = statistics['std'][8]
                    upperBoundary_altitudeRelative = altitudeRelativeAvg + 3*altitudeRelativeStd;lowerBoundary_altitudeRelative = altitudeRelativeAvg - 3*altitudeRelativeStd
                    if lowerBoundary_altitudeRelative <= inputData[r][8] <= upperBoundary_altitudeRelative:
                        sequential['altitudeRelative'].append('ok')
                    elif (lowerBoundary_altitudeRelative-altitudeRelativeAvg) <= inputData[r][8] < lowerBoundary_altitudeRelative or upperBoundary_altitudeRelative < inputData[r][8] <= (upperBoundary_altitudeRelative + altitudeRelativeAvg):
                        sequential['altitudeRelative'].append('mild')
                    elif (lowerBoundary_altitudeRelative-2*altitudeRelativeStd) <= inputData[r][8] < (lowerBoundary_altitudeRelative-altitudeRelativeStd) or (upperBoundary_altitudeRelative + altitudeRelativeStd) < inputData[r][8] <= (upperBoundary_altitudeRelative+2*altitudeRelativeStd):
                        sequential['altitudeRelative'].append('moderate')
                    else:
                        sequential['altitudeRelative'].append('critical')
                    
                    #------------#
                    ## 9.throttlePct:
                    throttlePctAvg = statistics['avg'][9];throttlePctStd = statistics['std'][9]
                    upperBoundary_throttlePct = throttlePctAvg + 3*throttlePctStd;lowerBoundary_throttlePct = throttlePctAvg - 3*throttlePctStd
                    if lowerBoundary_throttlePct <= inputData[r][9] <= upperBoundary_throttlePct:
                        sequential['throttlePct'].append('ok')
                    elif (lowerBoundary_throttlePct-throttlePctAvg) <= inputData[r][9] < lowerBoundary_throttlePct or upperBoundary_throttlePct < inputData[r][9] <= (upperBoundary_throttlePct + throttlePctAvg):
                        sequential['throttlePct'].append('mild')
                    elif (lowerBoundary_throttlePct-2*throttlePctStd) <= inputData[r][9] < (lowerBoundary_throttlePct-throttlePctStd) or (upperBoundary_throttlePct + throttlePctStd) < inputData[r][9] <= (upperBoundary_throttlePct+2*throttlePctStd):
                        sequential['throttlePct'].append('moderate')
                    else:
                        sequential['throttlePct'].append('critical')

                    individuals=pd.DataFrame(sequential)
                    weightedCluster.append(st.mode(individuals.iloc[0].values))
        return individuals,weightedCluster