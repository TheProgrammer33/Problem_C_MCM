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

def combineCSVs():
    goldDF = pd.read_csv('./Data/newGold.csv')
    btcDF = pd.read_csv('./Data/BCHAIN-MKPRU.csv')

    df = goldDF.join(btcDF['BTC Price'])
    #df = goldDF.insert(column='BTC Value', value=btcDF['Value'])

    df.to_csv('./Data/finalData.csv', index=False)
    

def insert_row(idx, df, df_insert):
    dfA = df.iloc[:idx]
    dfB = df.iloc[idx:]

    df = dfA.append(df_insert).append(dfB).reset_index(drop = True)

    return df

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

        goldDF = insert_row(positionInDF-1, goldDF,
            pd.DataFrame(np.array([[date, 
            goldDF['USD (PM)'][positionInDF-1]]]),
            columns=['Date', 'USD (PM)']))
        #goldDF.loc[positionInDF] = [date, goldDF[positionInDF-1]]

    goldDF.to_csv('./Data/newGold.csv', index=False)
    

def classifierCaller(classifierFunction):
    prediction = classifierFunction()

    print('Accuracy Score: ', round(accuracy_score(test[target], prediction)*100, 2),'%')

def setupData():
    btcGoldDF = pd.read_csv('./Data/')

    data = btcGoldDF[0:1]
    target = btcGoldDF[2]

    #dataTrain, dataTest, targetTrain, targetTest = train_test_split(data_mod, test_size=0.25)
    return train_test_split(btcGoldDF, test_size=0.15)

def naiveBayes(train, test, data, target):
    naiveBayes_model = GaussianNB()

    naiveBayes_model.fit(train[data], train[target])
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