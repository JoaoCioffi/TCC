# Main libraries
import anomalyDetection,clustering,loadData
import numpy as np
import colorama

# anomaly classifier:
module1 = anomalyDetection.findAnomaly()

# clustering method:
module2 = clustering.clusters()

# validating architecture with test data:
testData = loadData.loadData()
print(testData.sample(frac=1).reset_index(drop=True))