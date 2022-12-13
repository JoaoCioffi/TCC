[![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/Naereen/badges/)

![image](https://user-images.githubusercontent.com/60454486/207338037-10568815-161a-4f4b-9d22-4746c5dccde0.png)

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
