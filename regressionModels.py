# General imports
import pandas as pd
import numpy as np

# Model Training / Testing
from sklearn.model_selection import train_test_split
from sklearn import metrics

# Model Regession
#import xgboost
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import SGDRegressor
from sklearn.ensemble import GradientBoostingRegressor

DATA = ['GoldDaysSinceRise', 'GoldDaysSinceFall']
PREDICTION = 'Gold Price'

def setupData(numDataPoints, predictFuture):
    global BTCGOLDDF
    BTCGOLDDF = pd.read_csv('./Data/finalData.csv')
    configuredDataSizeDF = BTCGOLDDF.iloc[:numDataPoints]

    if (predictFuture):
        train, test = getFutureData(numDataPoints)
    else:
        train, test = train_test_split(configuredDataSizeDF, test_size=0.15)

    return train, test, DATA, PREDICTION

def setupDataRiseFall(numDataPoints):
    global BTCGOLDDF
    BTCGOLDDF = pd.read_csv('./Data/finalData.csv')

    for i in range(len(BTCGOLDDF) - 1):
        BTCGOLDDF.loc[i, "Gold Price"] = BTCGOLDDF["Gold Price"][i+1]
        BTCGOLDDF.loc[i, "BTC Price"] = BTCGOLDDF["BTC Price"][i+1]

    train, test = getFutureData(numDataPoints)

    return train, test, DATA, PREDICTION

def predictDay(model, day):
    train, test = getFutureData(day)

    return model.predict(test[DATA])

def retrainModel(model, day):
    train, test = getFutureData(day)

    model.fit(train[DATA], train[PREDICTION])

    return model

def DecisionTree(numDataPoints):
    #train, test, data, target = setupData(numDataPoints, True)
    train, test, data, target = setupDataRiseFall(numDataPoints)

    decisionTreeRegressor_model = DecisionTreeRegressor(random_state=1)

    decisionTreeRegressor_model.fit(train[data], train[target])

    #targetPrediction = decisionTreeRegressor_model.predict(test[data])

    # print('Mean Absolute Error:', metrics.mean_absolute_error(test[target], targetPrediction))  
    # print('Mean Squared Error:', metrics.mean_squared_error(test[target], targetPrediction))  
    # print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(test[target], targetPrediction)))

    return decisionTreeRegressor_model

def RandomForest(numDataPoints):
    train, test, data, target = setupData(numDataPoints, True)

    randomForestRegressor_model = RandomForestRegressor()

    randomForestRegressor_model.fit(train[data], train[target])

    targetPrediction = randomForestRegressor_model.predict(test[data])

    # print('Mean Absolute Error:', metrics.mean_absolute_error(test[target], targetPrediction))  
    # print('Mean Squared Error:', metrics.mean_squared_error(test[target], targetPrediction))  
    # print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(test[target], targetPrediction)))

    return targetPrediction

def MLPNN(numDataPoints):
    train, test, data, target = setupData(numDataPoints, True)

    multiLayerPerceptronRegressor_model = MLPRegressor(hidden_layer_sizes=(100,),
        activation="relu", learning_rate='adaptive', learning_rate_init=0.01)

    multiLayerPerceptronRegressor_model.fit(train[data], train[target])

    targetPrediction = multiLayerPerceptronRegressor_model.predict(test[data])

    # print('Mean Absolute Error:', metrics.mean_absolute_error(targetTest, targetPrediction))  
    # print('Mean Squared Error:', metrics.mean_squared_error(targetTest, targetPrediction))  
    # print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(targetTest, targetPrediction))) 

    return targetPrediction

def gradientBoosting(numDataPoints):
    train, test, data, target = setupData(numDataPoints, True)

    gradientBoosting_model = GradientBoostingRegressor(n_estimators=750, learning_rate=1)

    gradientBoosting_model.fit(train[data], train[target])

    targetPrediction = gradientBoosting_model.predict(test[data])

    return targetPrediction

def XGBoost(numDataPoints):
    train, test, data, target = setupData(numDataPoints, True)

    kNeighborsRegressor_model = KNeighborsRegressor()

    kNeighborsRegressor_model.fit(train[data], train[target])

    targetPrediction = kNeighborsRegressor_model.predict(test[data])

    return targetPrediction

def getFutureData(numDataPoints):
    train = BTCGOLDDF.iloc[:numDataPoints]
    test = BTCGOLDDF.iloc[numDataPoints:numDataPoints+1]

    return train, test

def setRiseFallDays(startDay):
    global BTCGOLDDF
    BTCGOLDDF = pd.read_csv('./Data/finalData.csv')

    global riseDays, fallDays
    riseDays = BTCGOLDDF[DATA[0]][startDay]
    fallDays = BTCGOLDDF[DATA[1]][startDay]

def addRiseFallDays(day, rise, fall):
    riseDays = rise
    fallDays = fall

    BTCGOLDDF.loc[day, DATA[0]] = riseDays
    BTCGOLDDF.loc[day, DATA[1]] = fallDays