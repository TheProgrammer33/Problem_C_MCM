# General imports
import pandas as pd
import numpy as np

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

def setupData(numDataPoints):
    btcGoldDF = pd.read_csv('./Data/finalData.csv')

    configuredDataSizeDF = btcGoldDF.iloc[:numDataPoints]

    data = ['Index']
    target = 'Gold Price'
    
    train, test = train_test_split(configuredDataSizeDF, test_size=0.15)

    return train, test, data, target

def classifierCaller(classifierFunction, numDataPoints):
    train, test, data, target = setupData(numDataPoints, True)
    
    prediction = classifierFunction(train, test, data, target)

    model_acc = round(accuracy_score(test[target], prediction)*100, 2)

    return numDataPoints, str(classifierFunction), model_acc

def naiveCaller(numDataPoints):
    train, test, data, target = setupData(numDataPoints)
    
    prediction = naiveBayes(train, test, data, target)

    model_acc = round(accuracy_score(test[target], prediction)*100, 2)

    return numDataPoints, str("Naive Bayes"), model_acc

def naiveBayes(train, test, data, target):
    naiveBayes_model = GaussianNB()

    randomList = [[0,1,1,2,4,5,3,2,1,4],[0,1,1,2,4,5,3,2,1,4]]
    naiveBayes_model.fit(train[data].values, train[target].astype('string'))
    
    return naiveBayes_model.predict(test[data])

def logisticRegression(train, test, data, target):
    logisticRegression_model = LogisticRegression()

    logisticRegression_model.fit(train[data], train[target])

    return logisticRegression_model.predict(test[data])

def decisionTree(train, test, data, target):
    decisionTreeClassifier_model = DecisionTreeClassifier()

    decisionTreeClassifier_model.fit(train[data], train[target])

    return decisionTreeClassifier_model.predict(test[data])

def randomForest(train, test, data, target):
    randomForestClassifier_model = RandomForestClassifier()

    randomForestClassifier_model.fit(train[data], train[target])

    return randomForestClassifier_model.predict(test[data])
