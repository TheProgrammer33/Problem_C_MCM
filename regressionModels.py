# General imports
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Model Training / Testing
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import SGDRegressor
from sklearn.ensemble import GradientBoostingRegressor

# Model Regession
from sklearn.tree import DecisionTreeRegressor

def setupData(numDataPoints, predictFuture):
    btcGoldDF = pd.read_csv('./Data/finalData.csv')

    configuredDataSizeDF = btcGoldDF.iloc[:numDataPoints]

    data = ['BTC Price']
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

def kNeighbors(numDataPoints):
    train, test, data, target = setupData(numDataPoints, True)

    kNeighborsRegressor_model = KNeighborsRegressor()

    kNeighborsRegressor_model.fit(train[data], train[target])

    targetPrediction = kNeighborsRegressor_model.predict(test[data])

    return targetPrediction

def bayesian(numDataPoints):
    train, test, data, target = setupData(numDataPoints, True)

    bayesianRidge_model = BayesianRidge()

    bayesianRidge_model.fit(train[data], train[target])

    targetPrediction = bayesianRidge_model.predict(test[data])

    return targetPrediction
    
def sdg(numDataPoints):
    train, test, data, target = setupData(numDataPoints, True)

    sdg_model = SGDRegressor()

    sdg_model.fit(train[data], train[target])

    targetPrediction = sdg_model.predict(test[data])

    return targetPrediction

def gradientBoosting(numDataPoints):
    train, test, data, target = setupData(numDataPoints, True)

    sdg_model = GradientBoostingRegressor(n_estimators=750, learning_rate=1)

    sdg_model.fit(train[data], train[target])

    targetPrediction = sdg_model.predict(test[data])

    return targetPrediction

def getFutureData(df, numDataPoints):
    train = df.iloc[:numDataPoints+1]
    test = df.iloc[numDataPoints:]

    return train, test
