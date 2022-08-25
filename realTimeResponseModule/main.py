# Main libraries
import anomalyDetection,clustering,loadData
import numpy as np
import pandas as pd
import colorama;colorama.init(autoreset=True)
from colorama import Fore, Back, Style
import time

startMain = time.time()

#____________// MAIN ARCHITECTURE //____________#
print('-='*35)
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
testData = testData.sample(frac=1).reset_index(drop=True).tail(30) #shuffling data and searching for the 30 last individuals
print(f'\n>> Input data for validation:\n{testData.head()}\n\n>> Statistics:\n{pd.DataFrame(statistics)}\n')

# checking for anomalies (can be editable cautiously):
time.sleep(1)
print('\n>> Starting anomaly detection...')
time.sleep(2)

anomalyDetectionInput = testData[['rollRate','pitchRate','yawRate']].values
clusteringInput = testData.values


print('\nValues:')

for r in range(anomalyDetectionInput.shape[0]): #rows
    rollRate,pitchRate,yawRate = anomalyDetectionInput[r][0],\
                                 anomalyDetectionInput[r][1],\
                                 anomalyDetectionInput[r][2]

    inputArray = np.array([[rollRate,pitchRate,yawRate]])
    print(f'\n* rollRate:{rollRate}dg/sec\n* pitchRate:{pitchRate}dg/sec\n* yawRate:{yawRate}dg/sec\n')

    def checkValues(inputArray=inputArray):
        anomalyResult = module1.predict(inputArray)
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
            print(f'\n* roll:{inputList[0]}dg\n* pitch:{inputList[1]}dg\n* heading:{inputList[2]}dg\n* rollRate:{inputList[3]}dg/s\n* pitchRate:{inputList[4]}dg/s\n* yawRate:{inputList[5]}dg/s\n* groundSpeed:{inputList[6]}m/s\n* climbRate:{inputList[7]}\n* altitudeRelative:{inputList[8]}m\n* throttlePct:{inputList[9]}%')
            
            inputArray = np.array([inputList])

            clusteringResult = module2.predict(inputArray)
            print(f'\n>> Main Cluster (KNN):{clusteringResult}')

            # For each 3 sequential anomalies, we need to get a Weighted Cluster to take our real-time decision
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
            ## 1.roll:
            rollAvg = statistics['Avg'][0]
            rollSTD = statistics['std'][0]
            upperBoundary_roll = rollAvg + rollSTD
            lowerBoundary_roll = -upperBoundary_roll
            if lowerBoundary_roll <= inputList[0] <= upperBoundary_roll:
                sequential['roll'].append(0) #normal range (level=0)
            elif (lowerBoundary_roll-rollSTD) <= inputList[0] < lowerBoundary_roll or upperBoundary_roll < inputList[0] <= (upperBoundary_roll + rollSTD):
                sequential['roll'].append(1) #over normal boundaries limited by 1std (level=1)
            elif (lowerBoundary_roll-2*rollSTD) <= inputList[0] < (lowerBoundary_roll-rollSTD) or (upperBoundary_roll + rollSTD) < inputList[0] <= (upperBoundary_roll+2*rollSTD):
                sequential['roll'].append(2) #between 1std and 2std (level=2)
            elif (lowerBoundary_roll-3*rollSTD) <= inputList[0] < (lowerBoundary_roll-2*rollSTD) or (upperBoundary_roll+2*rollSTD) < inputList[0] <= (upperBoundary_roll+3*rollSTD):
                sequential['roll'].append(3) #greater than 2std (level=3)
            
            ## 2.pitch:
            pitchAvg = statistics['Avg'][1]
            pitchSTD = statistics['std'][1]
            upperBoundary_pitch = pitchAvg + pitchSTD

            ## 3.heading:

            ## 4.rollRate:

            ## 5.pitchRate

            ## 6.yawRate:
            
            ## 7.groundSpeed:

            ## 8.climbRate

            ## 9.altitudeRelative:

            ## 10.throttlePct:

                
            print(sequential)
            
            del inputList

    checkValues()
    time.sleep(1)
    print('\n','_'*25)

endMain = time.time()
print(f'\n>> Time elapsed is {round((endMain-startMain),3)} seconds.\n   End of execution.\n')