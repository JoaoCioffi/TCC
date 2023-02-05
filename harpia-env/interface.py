from model import loadBinaries
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog

def GUI():

    root = tk.Tk()
    displayInfo=tk.Text(root)

    module1,module2,statistics=loadBinaries()

    def loadData():
        filePath = filedialog.askopenfilename(
        initialdir="/",
        title="Select file",
        filetypes=(
            ("CSV files", "*.csv"),
            ("all files", "*.*"))
        )

        if filePath:

            # aqui estou pegando n amostras aleatórias como teste de um arquivo .csv
            # (sugiro que o arquivo a ser lido siga o mesmo padrão, incluindo a ordem das colunas, que é o mesmo formato de log gerado do simulador, com as mesmas variáveis)
            testData = pd.read_csv(filePath,sep=";").sample(n=1).reset_index(drop=True)
            anomalyDetectionInput = testData[['rollRate','pitchRate','yawRate']].values
            clusteringInput = testData.values

            print(f'\nArquivo Carregado (csv):\n{testData}\n')

            # iterando sobre o conteúdo do arquivo
            for r in range(anomalyDetectionInput.shape[0]): # linhas
                rollRate,pitchRate,yawRate = anomalyDetectionInput[r][0],\
                                             anomalyDetectionInput[r][1],\
                                             anomalyDetectionInput[r][2]

                print(f'\n* rollRate:{round(rollRate,3)}dg/sec\n* pitchRate:{round(pitchRate,3)}dg/sec\n* yawRate:{round(yawRate,3)}dg/sec\n')

                # verificando anomalias
                inputArray = np.array([[rollRate,pitchRate,yawRate]])
                anomalyResult = module1.predict(inputArray)
                if anomalyResult[0] == 0:
                    displayData("Normal Pattern")
                else:
                    displayData("Found Anomalous Pattern! Starting clustering...")
                    inputList=[] # lista para armazenar as demais variáveis de voo
                    for c in range(clusteringInput.shape[1]): # colunas
                        inputList.append(clusteringInput[r][c])
                        print(f'\n* roll:{round(inputList[0],3)}dg\n* pitch:{round(inputList[1],3)}dg\n* heading:{round(inputList[2],3)}dg\n* rollRate:{round(inputList[3],3)}dg/s\n* pitchRate:{round(inputList[4],3)}dg/s\n* yawRate:{round(inputList[5],3)}dg/s\n* groundSpeed:{round(inputList[6],3)}m/s\n* climbRate:{round(inputList[7],3)}m/s\n* altitudeRelative:{round(inputList[8],3)}m\n* throttlePct:{round(inputList[9],3)}%')

                        inputArray = np.array([inputList])
                        clusteringResult = module2.predict(inputArray)
                        displayData(f"Main Cluster (k-Means): {clusteringResult}")

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
                        displayData(f'Individuals:\n{pd.DataFrame(sequential)}')

                        if weightedCluster[0] == 'ok':
                            print('\n>> Weighted Cluster: NORMAL LEVEL')
                            displayData('Weighted Cluster: NORMAL LEVEL')
                        elif weightedCluster[0] == 'mild':
                            print('\n>> Weighted Cluster: MILD LEVEL')
                            displayData('Weighted Cluster: MILD LEVEL')
                        elif weightedCluster[0] == 'moderate':
                            print('\n>> Weighted Cluster: MODERATE LEVEL')
                            displayData('Weighted Cluster: MODERATE LEVEL')
                        else:
                            print('\n>> Weighted Cluster: CRITICAL LEVEL')
                            displayData('Weighted Cluster: CRITICAL LEVEL')
                    
    
    def displayData(data):
        # displayInfo.delete("1.0",tk.END)
        try:
            displayInfo.insert("1.0",f'\n[INFO]\n{data.to_string()}\n')
        except:
            displayInfo.insert("1.0",f'\n[INFO]\n{str(data)}\n')
        displayInfo.pack()
    
    loadButton=tk.Button(root,text="Load Data",command=loadData)
    loadButton.pack()
    root.mainloop()