[![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/Naereen/badges/)

![image](https://user-images.githubusercontent.com/60454486/207338037-10568815-161a-4f4b-9d22-4746c5dccde0.png)

Current Project Tree:
``` 
.
├── cioffi_jr_tcc_sjbv.pdf
├── flowchart.png
├── mainArchitecture
│   ├── 1.WeatherForecasting
│   │   ├── METAR_TCC
│   │   │   ├── Data
│   │   │   │   └── SBRP.csv
│   │   │   ├── readme.md
│   │   │   ├── Scripts
│   │   │   │   ├── JupyterNotebook
│   │   │   │   │   ├── Metar_Predictor.ipynb
│   │   │   │   │   └── SBRP.csv
│   │   │   │   └── Metar_Predictor.py
│   │   │   └── SystemOutput
│   │   │       ├── METAR.joblib
│   │   │       └── tree
│   │   └── Readme.md
│   ├── 2.AnomalyDetection
│   │   ├── Data
│   │   │   ├── LSTM_output.csv
│   │   │   └── RawData.csv
│   │   ├── ExportedModels_Joblib
│   │   │   ├── anomalyDetector.joblib
│   │   │   └── LSTM.joblib
│   │   ├── readme.md
│   │   ├── ROS_Fundamentals
│   │   │   ├── CMakeLists.txt
│   │   │   ├── hello.cpp
│   │   │   ├── package.xml
│   │   │   └── pubvel.cpp
│   │   └── Scripts
│   │       ├── 2_anomalydetection_lstm.py
│   │       └── JupyterNotebook
│   │           ├── 2_AnomalyDetection_LSTM.ipynb
│   │           └── postProcessing
│   │               ├── LSTM_output.csv
│   │               └── postProcessing.ipynb
│   └── 3.ClusteringAlgorythm
│       ├── Data
│       │   └── LSTM_output.csv
│       ├── ExportedModels_Joblib
│       │   └── clusters.joblib
│       ├── readme.md
│       └── Scripts
│           └── JupyterNotebook
│               └── KMeans_Clustering
│                   ├── KMeans_Clustering.ipynb
│                   └── LSTM_output.csv
├── pip_dependencies
│   └── dependencies.txt
├── projectTree.txt
├── README.md
├── realTimeResponseModule
│   ├── anomalyDetection.py
│   ├── clustering.py
│   ├── dependencies
│   │   ├── anomalyDetector.joblib
│   │   ├── clusters.joblib
│   │   └── rawData.csv
│   ├── DJI_Tello_Drone
│   │   ├── constants.py
│   │   ├── dependencies
│   │   │   ├── bckp
│   │   │   │   ├── enforce_types.py
│   │   │   │   ├── __init__.py
│   │   │   │   ├── __pycache__
│   │   │   │   │   ├── enforce_types.cpython-38.pyc
│   │   │   │   │   ├── __init__.cpython-38.pyc
│   │   │   │   │   ├── swarm.cpython-38.pyc
│   │   │   │   │   └── tello.cpython-38.pyc
│   │   │   │   ├── swarm.py
│   │   │   │   └── tello.py
│   │   │   ├── fv_statistics.csv
│   │   │   └── readme.txt
│   │   ├── main.py
│   │   ├── missions.py
│   │   ├── __pycache__
│   │   │   ├── constants.cpython-38.pyc
│   │   │   └── missions.cpython-38.pyc
│   │   ├── README.md
│   │   └── Tello SDK Documentation EN_1.3_1122.pdf
│   ├── loadData.py
│   ├── main.py
│   ├── METAR_module
│   │   ├── dependencies
│   │   │   └── GradientBooster.pkl
│   │   ├── main.py
│   │   ├── predictor.py
│   │   ├── __pycache__
│   │   │   └── predictor.cpython-310.pyc
│   │   └── relations.pdf
│   ├── NoiseGenerator.py
│   ├── __pycache__
│   │   ├── anomalyDetection.cpython-310.pyc
│   │   ├── anomalyDetection.cpython-38.pyc
│   │   ├── clustering.cpython-310.pyc
│   │   ├── clustering.cpython-38.pyc
│   │   ├── loadData.cpython-310.pyc
│   │   ├── loadData.cpython-38.pyc
│   │   ├── NoiseGenerator.cpython-310.pyc
│   │   └── NoiseGenerator.cpython-38.pyc
│   └── README.md
└── SECURITY.md

32 directories, 70 files
```

# About TCC

1. General:
    - This repository content is related to my Graduation's Final Paper
    - Course: Bachelor Degree in Aeronautical Engineering at Sao Paulo State University-"Júlio de Mesquita Filho" (UNESP)
    - Paper Title: "Sistema de Planejamento de Voo Autônomo Utilizando Inteligência Artificial" (PT-BR) | "Autonomous Flight Planning System Using Artificial Intelligence" (US-EN)

2. Architecture and Objective:
The general objective of the work is to create an integrated system for mission planning of
an autonomous aerial vehicle, from the pre-flight to real-time decision making. This goal
can be specifically extended as follows:
    - **First module of the architecture:** Implementation of supervised learning (multiple regression) for forecasting weather data at least 1 hour before the flight. In case of having the right conditions, the decision to execute the mission will be on responsible of the mission operator.
    - **Anomaly detection module:** use of artificial neural networks to understand the
    flight data (time dependence between variables) and identification of anomalous patterns. Case
    a dataset is within a faulty time interval, the real-time decision will be
    made according to the levels of these behavioral patterns.
    - **Classification module in sublevels:** use of unsupervised learning for the
    proper grouping (clustering) of previously identified incorrect patterns. In this
    step, the system should be able to subdivide into 3 large groups (or levels): lightweight categories,
    moderate and critical levels of these anomalies.
