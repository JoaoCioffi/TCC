# Main libraries
import anomalyDetection,clustering,loadData
import numpy as np
import pandas as pd
import colorama;colorama.init(autoreset=True)
import termcolor
from colorama import Fore, Back, Style
import progressbar
import time

startMain = time.time()

#____________// MAIN ARCHITECTURE //____________#
print('-='*50)
print('\n\t\t<< Real Time Response Analysis >>\n\n')


# anomaly classifier (static):
start_1 = time.time()
module1 = anomalyDetection.findAnomaly()
end_1 = time.time()
print(f'\n>> Loaded Anomaly Detection Module in {round((end_1-start_1),3)} seconds.\n')


# clustering method (static):
start_2 = time.time()
module2 = clustering.clusters()
end_2 = time.time()
print(f'\n>> Loaded Clustering Module in {round((end_2-start_2),3)} seconds.\n')

#____________// VALIDATION //____________#
# test data (can be editable):
testData,statistics = loadData.loadData(printColumnNames=True)
testData = testData.sample(frac=1).reset_index(drop=True).tail(60) #shuffling data and searching for the 30 last individuals
print(f'\n>> Input data for validation:\n{testData.head()}\n\n>> Statistics:\n{pd.DataFrame(statistics)}\n')

# checking for anomalies (can be editable cautiously):
time.sleep(1)
print('\n>> Starting anomaly detection...\n')
time.sleep(2)

anomalyDetectionInput = testData[['rollRate','pitchRate','yawRate']].values
clusteringInput = testData.values

# progress bar object
widgets = [' Reading data: ', progressbar.RotatingMarker()]
bar = progressbar.ProgressBar(widgets=widgets).start()

# iteration for reading data (delay = 1s)
for r in range(anomalyDetectionInput.shape[0]): #rows
    bar.update(r) #bar update for each 'r' in range
    rollRate,pitchRate,yawRate = anomalyDetectionInput[r][0],\
                                 anomalyDetectionInput[r][1],\
                                 anomalyDetectionInput[r][2]

    inputArray = np.array([[rollRate,pitchRate,yawRate]])
    print(f'\n* rollRate:{rollRate}dg/sec\n* pitchRate:{pitchRate}dg/sec\n* yawRate:{yawRate}dg/sec\n')

    def checkValues(inputArray=inputArray):
        anomalyResult = module1.predict(inputArray) #loaded model prediction (anomaly classification)
        if anomalyResult[0] == 0:
            print(Fore.BLACK + Back.GREEN + "Normal Pattern")
            print(Style.RESET_ALL)

        else:
            print(Fore.BLACK + Back.RED + "Found Anomalous Pattern!")
            print(Style.RESET_ALL)
            print('\n>> Starting clustering...')

            inputList = [] # will append the current flight data (all of them)
            for c in range(clusteringInput.shape[1]): #columns
                inputList.append(clusteringInput[r][c])
            print(f'\n* roll:{inputList[0]}dg\n* pitch:{inputList[1]}dg\n* heading:{inputList[2]}dg\n* rollRate:{inputList[3]}dg/s\n* pitchRate:{inputList[4]}dg/s\n* yawRate:{inputList[5]}dg/s\n* groundSpeed:{inputList[6]}m/s\n* climbRate:{inputList[7]}m/s\n* altitudeRelative:{inputList[8]}m\n* throttlePct:{inputList[9]}%')
            
            inputArray = np.array([inputList])

            clusteringResult = module2.predict(inputArray) #loaded model prediction (anomaly clustering)
            print(f'\n>> Main Cluster (KNN):{clusteringResult}')

            # For each 3 sequential candidates, we need to get a Weighted Cluster to take our real-time decision
            sequential = {'roll':[],
                          'pitch':[],
                          'heading':[],
                          'rollRate':[],
                          'pitchRate':[],
                          'yawRate':[],
                          'groundSpeed':[],
                          'climbRate':[],
                          'altitudeRelative':[],
                          'throttlePct':[]};weightedCluster = []
            
            #------------#
            ## 0.roll:
            rollAvg = statistics['Avg'][0];rollStd = statistics['std'][0] #mean() and std()
            upperBoundary_roll = rollAvg + 3*rollStd;lowerBoundary_roll = rollAvg - 3*rollStd #boundaries: mean() +/- 3std()
            
            if lowerBoundary_roll <= inputList[0] <= upperBoundary_roll:
                sequential['roll'].append('ok') #normal range (level=0)
            elif (lowerBoundary_roll-rollStd) <= inputList[0] < lowerBoundary_roll or upperBoundary_roll < inputList[0] <= (upperBoundary_roll + rollStd):
                sequential['roll'].append('mild') #over normal boundaries limited by 1std (level=1)
            elif (lowerBoundary_roll-2*rollStd) <= inputList[0] < (lowerBoundary_roll-rollStd) or (upperBoundary_roll + rollStd) < inputList[0] <= (upperBoundary_roll+2*rollStd):
                sequential['roll'].append('moderate') #between 1std and 2std (level=2)
            else:
                sequential['roll'].append('critical') #greater than 2std (level=3)
            
            #------------#
            ## 1.pitch:
            pitchAvg = statistics['Avg'][1];pitchStd = statistics['std'][1]
            upperBoundary_pitch = pitchAvg + 3*pitchStd;lowerBoundary_pitch = pitchAvg - 3*pitchStd
            
            if lowerBoundary_pitch <= inputList[1] <= upperBoundary_pitch:
                sequential['pitch'].append('ok')
            elif (lowerBoundary_pitch-pitchStd) <= inputList[1] < lowerBoundary_pitch or upperBoundary_pitch < inputList[1] <= (upperBoundary_pitch + pitchStd):
                sequential['pitch'].append('mild')
            elif (lowerBoundary_pitch-2*pitchStd) <= inputList[1] < (lowerBoundary_pitch-pitchStd) or (upperBoundary_pitch + pitchStd) < inputList[1] <= (upperBoundary_pitch+2*pitchStd):
                sequential['pitch'].append('moderate')
            else:
                sequential['pitch'].append('critical')

            #------------#
            ## 2.heading:
            headingAvg = statistics['Avg'][2];headingStd = statistics['std'][2]
            upperBoundary_heading = headingAvg + 3*headingStd;lowerBoundary_heading = headingAvg - 3*headingStd

            if lowerBoundary_heading <= inputList[2] <= upperBoundary_heading:
                sequential['heading'].append('ok')
            elif (lowerBoundary_heading-headingStd) <= inputList[2] < lowerBoundary_heading or upperBoundary_heading < inputList[2] <= (upperBoundary_heading + headingStd):
                sequential['heading'].append('mild')
            elif (lowerBoundary_heading-2*headingStd) <= inputList[2] < (lowerBoundary_heading-headingStd) or (upperBoundary_pitch + headingStd) < inputList[2] <= (upperBoundary_heading+2*headingStd):
                sequential['heading'].append('moderate')
            else:
                sequential['heading'].append('critical')

            #------------#
            ## 3.rollRate:
            rollRateAvg = statistics['Avg'][3];rollRateStd = statistics['std'][3]
            upperBoundary_rollRate = rollRateAvg + 3*rollRateStd;lowerBoundary_rollRate = rollRateAvg - 3*rollRateStd

            if lowerBoundary_rollRate <= inputList[3] <= upperBoundary_rollRate:
                sequential['rollRate'].append('ok')
            elif (lowerBoundary_rollRate-rollRateStd) <= inputList[3] < lowerBoundary_rollRate or upperBoundary_rollRate < inputList[3] <= (upperBoundary_rollRate + rollRateStd):
                sequential['rollRate'].append('mild')
            elif (lowerBoundary_rollRate-2*rollRateStd) <= inputList[3] < (lowerBoundary_rollRate-rollRateStd) or (upperBoundary_rollRate + rollRateStd) < inputList[3] <= (upperBoundary_rollRate+2*rollRateStd):
                sequential['rollRate'].append('moderate')
            else:
                sequential['rollRate'].append('critical')

            #------------#
            ## 4.pitchRate
            pitchRateAvg = statistics['Avg'][4];pitchRateStd = statistics['std'][4]
            upperBoundary_pitchRate = pitchRateAvg + 3*pitchRateStd;lowerBoundary_pitchRate = pitchRateAvg - 3*pitchRateStd

            if lowerBoundary_pitchRate <= inputList[4] <= upperBoundary_pitchRate:
                sequential['pitchRate'].append('ok')
            elif (lowerBoundary_pitchRate-pitchRateStd) <= inputList[4] < lowerBoundary_pitchRate or upperBoundary_pitchRate < inputList[4] <= (upperBoundary_pitchRate + pitchRateStd):
                sequential['pitchRate'].append('mild')
            elif (lowerBoundary_pitchRate-2*pitchRateStd) <= inputList[4] < (lowerBoundary_pitchRate-pitchRateStd) or (upperBoundary_pitchRate + pitchRateStd) < inputList[4] <= (upperBoundary_pitchRate+2*pitchRateStd):
                sequential['pitchRate'].append('moderate')
            else:
                sequential['pitchRate'].append('critical')

            #------------#
            ## 5.yawRate:
            yawRateAvg = statistics['Avg'][5];yawRateStd = statistics['std'][5]
            upperBoundary_yawRate = yawRateAvg + 3*yawRateStd;lowerBoundary_yawRate = yawRateAvg - 3*yawRateStd

            if lowerBoundary_yawRate <= inputList[5] <= upperBoundary_yawRate:
                sequential['yawRate'].append('ok')
            elif (lowerBoundary_yawRate-yawRateAvg) <= inputList[5] < lowerBoundary_yawRate or upperBoundary_yawRate < inputList[5] <= (upperBoundary_yawRate + yawRateAvg):
                sequential['yawRate'].append('mild')
            elif (lowerBoundary_yawRate-2*yawRateStd) <= inputList[5] < (lowerBoundary_yawRate-yawRateStd) or (upperBoundary_yawRate + yawRateStd) < inputList[5] <= (upperBoundary_yawRate+2*yawRateStd):
                sequential['yawRate'].append('moderate')
            else:
                sequential['yawRate'].append('critical')

            
            #------------#
            ## 6.groundSpeed:
            groundSpeedAvg = statistics['Avg'][6];groundSpeedStd = statistics['std'][6]
            upperBoundary_groundSpeed = groundSpeedAvg + 3*groundSpeedStd;lowerBoundary_groundSpeed = groundSpeedAvg - 3*groundSpeedStd

            if lowerBoundary_groundSpeed <= inputList[6] <= upperBoundary_groundSpeed:
                sequential['groundSpeed'].append('ok')
            elif (lowerBoundary_groundSpeed-groundSpeedAvg) <= inputList[6] < lowerBoundary_groundSpeed or upperBoundary_groundSpeed < inputList[6] <= (upperBoundary_groundSpeed + groundSpeedAvg):
                sequential['groundSpeed'].append('mild')
            elif (lowerBoundary_groundSpeed-2*groundSpeedStd) <= inputList[6] < (lowerBoundary_groundSpeed-groundSpeedStd) or (upperBoundary_groundSpeed + groundSpeedStd) < inputList[6] <= (upperBoundary_groundSpeed+2*groundSpeedStd):
                sequential['groundSpeed'].append('moderate')
            else:
                sequential['groundSpeed'].append('critical')

            #------------#
            ## 7.climbRate
            climbRateAvg = statistics['Avg'][7];climbRateStd = statistics['std'][7]
            upperBoundary_climbRate = climbRateAvg + 3*climbRateStd;lowerBoundary_climbRate = climbRateAvg - 3*climbRateStd

            if lowerBoundary_climbRate <= inputList[7] <= upperBoundary_climbRate:
                sequential['climbRate'].append('ok')
            elif (lowerBoundary_climbRate-climbRateAvg) <= inputList[7] < lowerBoundary_climbRate or upperBoundary_climbRate < inputList[7] <= (upperBoundary_climbRate + climbRateAvg):
                sequential['climbRate'].append('mild')
            elif (lowerBoundary_climbRate-2*climbRateStd) <= inputList[7] < (lowerBoundary_climbRate-climbRateStd) or (upperBoundary_climbRate + climbRateStd) < inputList[7] <= (upperBoundary_climbRate+2*climbRateStd):
                sequential['climbRate'].append('moderate')
            else:
                sequential['climbRate'].append('critical')


            #------------#
            ## 8.altitudeRelative:
            altitudeRelativeAvg = statistics['Avg'][8];altitudeRelativeStd = statistics['std'][8]
            upperBoundary_altitudeRelative = altitudeRelativeAvg + 3*altitudeRelativeStd;lowerBoundary_altitudeRelative = altitudeRelativeAvg - 3*altitudeRelativeStd

            if lowerBoundary_altitudeRelative <= inputList[8] <= upperBoundary_altitudeRelative:
                sequential['altitudeRelative'].append('ok')
            elif (lowerBoundary_altitudeRelative-altitudeRelativeAvg) <= inputList[8] < lowerBoundary_altitudeRelative or upperBoundary_altitudeRelative < inputList[8] <= (upperBoundary_altitudeRelative + altitudeRelativeAvg):
                sequential['altitudeRelative'].append('mild')
            elif (lowerBoundary_altitudeRelative-2*altitudeRelativeStd) <= inputList[8] < (lowerBoundary_altitudeRelative-altitudeRelativeStd) or (upperBoundary_altitudeRelative + altitudeRelativeStd) < inputList[8] <= (upperBoundary_altitudeRelative+2*altitudeRelativeStd):
                sequential['altitudeRelative'].append('moderate')
            else:
                sequential['altitudeRelative'].append('critical')

            #------------#
            ## 9.throttlePct:
            throttlePctAvg = statistics['Avg'][9];throttlePctStd = statistics['std'][9]
            upperBoundary_throttlePct = throttlePctAvg + 3*throttlePctStd;lowerBoundary_throttlePct = throttlePctAvg - 3*throttlePctStd

            if lowerBoundary_throttlePct <= inputList[9] <= upperBoundary_throttlePct:
                sequential['throttlePct'].append('ok')
            elif (lowerBoundary_throttlePct-throttlePctAvg) <= inputList[9] < lowerBoundary_throttlePct or upperBoundary_throttlePct < inputList[9] <= (upperBoundary_throttlePct + throttlePctAvg):
                sequential['throttlePct'].append('mild')
            elif (lowerBoundary_throttlePct-2*throttlePctStd) <= inputList[9] < (lowerBoundary_throttlePct-throttlePctStd) or (upperBoundary_throttlePct + throttlePctStd) < inputList[9] <= (upperBoundary_throttlePct+2*throttlePctStd):
                sequential['throttlePct'].append('moderate')
            else:
                sequential['throttlePct'].append('critical')

            #------------#
            ## weighted cluster:
            weightedCluster.append(pd.DataFrame(sequential).mode(axis=0).values[0][0]) #weighted cluster over previous data
            

            print(f'\n>> Individuals:\n{pd.DataFrame(sequential)}')
            if weightedCluster[0] == ' ':
                print('\nWeighted Cluster: ' + termcolor.colored("Normal Level", "green", attrs=['bold']) + '\n') #keep flying
            elif weightedCluster[0] == 'mild':
                print('\nWeighted Cluster: ' + termcolor.colored("Mild Level", "blue", attrs=['bold']) + '\n') #keep flying cautiously
            elif weightedCluster[0] == 'moderate':
                print('\nWeighted Cluster: ' + termcolor.colored("Moderate Level", "yellow", attrs=['bold'])) #go to the next waypoint
            else:
                print('\nWeighted Cluster: ' + termcolor.colored("Critical Level", "red", attrs=['bold']) + '\n') #land on this location
                abort = input('\n>> Abort Mission? [Y/N] -> ').upper() #user decision
                return abort
            return weightedCluster
    
    log2Terminal = checkValues() #calling function and running script (terminal output)
    print(log2Terminal)

    time.sleep(1) #delay = 1s (approximately a real drone response rating)
    print('\n','.'*37,'\n')
    if log2Terminal == 'Y':
        print(Fore.BLACK + Back.YELLOW + "\nAborted Mission!")
        print(Style.RESET_ALL)
        break
    else:
        continue

endMain = time.time()
print(f'\n>> Time elapsed is {round((endMain-startMain),3)} seconds.\n   End of execution.\n')