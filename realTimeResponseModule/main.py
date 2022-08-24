# Main libraries
import anomalyDetection,clustering,loadData
import numpy as np
import colorama;colorama.init(autoreset=True)
from colorama import Fore, Back, Style
import time

#____________// MAIN ARCHITECTURE //____________#

print('-='*35)
print('\n\t\t<< Real Time Response Analysis >>\n\n')


# anomaly classifier (static):
start = time.time()
module1 = anomalyDetection.findAnomaly()
end = time.time()
print(f'\n>> Loaded Anomaly Detection Module in {round((end-start),3)} seconds.\n')


# clustering method (static):
start = time.time()
module2 = clustering.clusters()
end = time.time()
print(f'\n>> Loaded Clustering Module in {round((end-start),3)} seconds.\n')

#____________// VALIDATION //____________#

# test data (can be editable):
testData = loadData.loadData(printColumnNames=True)
testData = testData.sample(frac=1).reset_index(drop=True).tail(30) #shuffling data and searching for the 30 last individuals
print(f'\n>> Input data for validation:\n{testData.head()}\n')

# checking for anomalies:
time.sleep(1)
print('\n>> Starting anomaly detection...')
time.sleep(2)

anomalyDetectionInput = testData[['rollRate','pitchRate','yawRate']].values
print('\nValues:')
for r in range(anomalyDetectionInput.shape[0]): #rows
    rollRate,pitchRate,yawRate = anomalyDetectionInput[r][0],\
                                 anomalyDetectionInput[r][1],\
                                 anomalyDetectionInput[r][2]

    inputArray = np.array([[rollRate,pitchRate,yawRate]])
    print(f'\n* rollRate:{rollRate}\n* pitchRate:{pitchRate}\n* yawRate:{yawRate}\n')

    def checkValues(inputArray=inputArray):
        anomalyResult = module1.predict(inputArray)
        if anomalyResult[0] == 0:
            print(Fore.BLACK + Back.GREEN + "Normal Pattern")
            print(Style.RESET_ALL)
        else:
            print(Fore.BLACK + Back.RED + "Found Anomaly Pattern!")
            print(Style.RESET_ALL)

    checkValues()
    time.sleep(1)
    print('\n','_'*25)