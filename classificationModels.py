# General imports
import pandas as pd
import numpy as np
import dataAnalyzer

# Data cleaning
from sklearn.preprocessing import StandardScaler

# Model Training / Testing
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import metrics

# Model Classifiers
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

def fillGold():
    goldDF = pd.read_csv('./Data/LBMA-GOLD.csv')
    btcDF = pd.read_csv('./Data/BCHAIN-MKPRU.csv')

    # previousDay = goldDF['Date'][0]
    # currentDay = goldDF['Date'][1]
    # for i in range(0, btcDF.size()):
    #     if int(dataAnalyzer.getDay(currentDay)) - int(dataAnalyzer.getDay(previousDay)) > 0:

    missingDates = dataAnalyzer.findMissingDates()

    for date in missingDates:
        positionInDF = dataAnalyzer.getDFPosition(date)

        print(positionInDF)



def setupData():


    pima = pd.read_csv("CSV/pima-indians-diabetes.csv")

    data_mod = pima[(pima.BloodP != 0) & (pima.BMI != 0) & (pima.Glucose != 0)]

    data = ['Pregnancies', 'Glucose', 'BloodP', 'SkinThick', 'BMI', 'Age', 'Insulin', 'DiabetesPedigreeFunction']
    target = "Outcome"

    #dataTrain, dataTest, targetTrain, targetTest = train_test_split(data_mod, test_size=0.25)
    train, test = train_test_split(data_mod, test_size=0.25)

    standardScaler = StandardScaler()
    dataTrainScaled=standardScaler.fit_transform(train[data])
    dataTestScaled=standardScaler.transform(test[data])