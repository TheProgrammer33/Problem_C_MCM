# General imports
import pandas as pd
import numpy as np
import dataAnalyzer

# Data cleaning
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

# Model Training / Testing
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import metrics

# Model Classifiers
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

def combineCSVs():
    goldDF = pd.read_csv('./Data/newGold.csv')
    btcDF = pd.read_csv('./Data/BCHAIN-MKPRU.csv')

    df = goldDF.join(btcDF['BTC Price'])

    df.to_csv('./Data/finalData.csv', index=True)

def insert_row(idx, df, df_insert):
    dfA = df.iloc[:idx]
    dfB = df.iloc[idx:]

    df = dfA.append(df_insert).append(dfB).reset_index(drop = True)

    return df

def fillGold():
    goldDF = pd.read_csv('./Data/fixedGold.csv')

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

def fixGold():
    goldDF = pd.read_csv('./Data/LBMA-GOLD.csv')

    # previousDay = goldDF['Date'][0]
    # currentDay = goldDF['Date'][1]
    # for i in range(0, btcDF.size()):
    #     if int(dataAnalyzer.getDay(currentDay)) - int(dataAnalyzer.getDay(previousDay)) > 0:

    positions, dates = dataAnalyzer.getMissingPriceDates(goldDF)

    for i in range(len(positions)):
        #goldDF['USD (PM)'][position] = goldDF['USD (PM)'][position-1]
        goldDF.loc[positions[i]] = dates[i], goldDF['USD (PM)'][positions[i]-1]
        #goldDF.loc[positionInDF] = [date, goldDF[positionInDF-1]]

    goldDF.to_csv('./Data/fixedGold.csv', index=False)

def setupData(numDataPoints, predictFuture):
    btcGoldDF = pd.read_csv('./Data/finalData.csv')

    configuredDataSizeDF = btcGoldDF.iloc[:numDataPoints]

    data = ['Index']
    target = 'Gold Price'

    if (predictFuture):
        train, test = getFutureData(btcGoldDF, numDataPoints)
    else:
        train, test = train_test_split(configuredDataSizeDF, test_size=0.15)

    return train, test, data, target#, trainTargetEncoded, testTargetEncoded

def regressionAttempt(numDataPoints):
    train, test, data, target = setupData(numDataPoints, True)

    decisionTreeRegressor_model = DecisionTreeRegressor()

    decisionTreeRegressor_model.fit(train[data], train[target])

    targetPrediction = decisionTreeRegressor_model.predict(test[data])

    # print('Mean Absolute Error:', metrics.mean_absolute_error(test[target], targetPrediction))  
    # print('Mean Squared Error:', metrics.mean_squared_error(test[target], targetPrediction))  
    # print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(test[target], targetPrediction)))

    return targetPrediction

def classifierCaller(classifierFunction, numDataPoints):
    train, test, data, target = setupData(numDataPoints)
    
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

    # multiLayerPerceptronClassifier_model.fit(dataTrainScaled, train[target])

    # targetPrediction = multiLayerPerceptronClassifier_model.predict(dataTestScaled)

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

def getFutureData(df, numDataPoints):
    train = df.iloc[:numDataPoints]
    test = df.iloc[[numDataPoints+1]]

    return train, test