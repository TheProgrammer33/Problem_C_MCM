# General imports
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Model Training / Testing
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor

# Model Regession
from sklearn.tree import DecisionTreeRegressor

def setupData(numDataPoints, predictFuture):
    btcGoldDF = pd.read_csv('./Data/finalData.csv')

    configuredDataSizeDF = btcGoldDF.iloc[:numDataPoints]

    data = ['Index']
    target = 'Gold Price'

    if (predictFuture):
        train, test = getFutureData(btcGoldDF, numDataPoints)
    else:
        train, test = train_test_split(configuredDataSizeDF, test_size=0.15)

    return train, test, data, target

def DecisionTree(numDataPoints):
    train, test, data, target = setupData(numDataPoints, True)

    decisionTreeRegressor_model = DecisionTreeRegressor()

    decisionTreeRegressor_model.fit(train[data], train[target])

    targetPrediction = decisionTreeRegressor_model.predict(test[data])

    # print('Mean Absolute Error:', metrics.mean_absolute_error(test[target], targetPrediction))  
    # print('Mean Squared Error:', metrics.mean_squared_error(test[target], targetPrediction))  
    # print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(test[target], targetPrediction)))

    return targetPrediction

def RandomForest(numDataPoints):
    train, test, data, target = setupData(numDataPoints, True)

    randomForestRegressor_model = RandomForestRegressor()

    randomForestRegressor_model.fit(train[data], train[target])

    targetPrediction = randomForestRegressor_model.predict(test[data])

    # print('Mean Absolute Error:', metrics.mean_absolute_error(test[target], targetPrediction))  
    # print('Mean Squared Error:', metrics.mean_squared_error(test[target], targetPrediction))  
    # print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(test[target], targetPrediction)))

    return targetPrediction

def kNeighbors(numDataPoints):
    train, test, data, target = setupData(numDataPoints, True)

    kNeighborsRegressor_model = KNeighborsRegressor()

    kNeighborsRegressor_model.fit(train[data], train[target])

    targetPrediction = kNeighborsRegressor_model.predict(test[data])

    return targetPrediction

def getFutureData(df, numDataPoints):
    train = df.iloc[:numDataPoints]
    test = df.iloc[[numDataPoints+1]]

    return train, test

