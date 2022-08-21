# Main Libraries
import os
import joblib

# Anomaly Detection Module:
def findAnomaly(relative_path="realTimeResponseModule/dependencies",filename="anomalyDetector.joblib")
    os.chdir(relative_path)
    findAnomalyAlg = joblib.load(filename)
    return findAnomalyAlg

# Clustering Module:
def clusters(relative_path="realTimeResponseModule/dependencies",filename="clusters.joblib")
    os.chdir(relative_path)
    clusteringAlg = joblib.load(filename)
    return clusteringAlg