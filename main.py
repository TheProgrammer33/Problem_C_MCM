import pandas as pd
import time
from multiprocessing import Process

import dataAnalyzer, dataCleaner
import regressionModels
import classificationModels
import priceEffect
import wallet

import matplotlib.pyplot as plt
import math
from scipy.signal import savgol_filter

NUM_PROC = 4

def predictDays(startDay):
    results = {"Price": [], "Prediction": [], "Actual": [], "Accurate": []}

    for trainingDays in range(startDay, len(btcGoldDF)-1):
        lastTrainingDayPrice = btcGoldDF["Gold Price"][trainingDays]
        predictionForNextDay = getRiseFall(lastTrainingDayPrice, regressionModels.DecisionTree(trainingDays)[0])
        actualNextDay = getRiseFall(lastTrainingDayPrice, btcGoldDF["Gold Price"][trainingDays+1])

        results["Price"].append(lastTrainingDayPrice)
        results["Prediction"].append(predictionForNextDay)
        results["Actual"].append(actualNextDay)
        results["Accurate"].append(1 if predictionForNextDay == actualNextDay else 0)

    summedPredictions = 0
    for accurate in results["Accurate"]:
        summedPredictions += accurate * 100
    
    accuracy = summedPredictions / len(results["Accurate"])

    if (accuracy > 50):
        resultDF = pd.DataFrame(results)
        resultDF.to_csv('./Data/GradientBoosterGold/trainingResults' + str(startDay) +'.csv', index=False, columns=["Price", "Prediction", "Actual", "Accurate"])

        outfile = open('./Data/GradientBoosterGold/trainingResults' + str(startDay) + '.csv', "a")
        outfile.write(str(accuracy))
        outfile.close()
    else:
        outfile = open('./Data/GradientBoosterGold/badTrainingResults.csv', "a")
        outfile.write(str(startDay) + ": " + str(accuracy) + "\n")
        outfile.close()

def train():
    # Change range values (start day, lastStartDay)
    for startDay in range(15, 300, NUM_PROC):
        jobs = []

        for i in range(NUM_PROC):
            process = Process(
                target=predictDays, 
                args=(startDay+i,)
            )
            jobs.append(process)

        for j in jobs:
            j.start()

        for j in jobs:
            j.join()

# The predictions are the same past the first day. It's not predicting future days, just a single value which doesn't help
# It needs to give values for each day, not one value for every day
# Figure out why the data going into the model isn't training it to predict properly

def main():
    print("Starting...")

    #dataSmoothingGold()

    dataCleaner.combineCSVs()

    global btcGoldDF
    btcGoldDF = pd.read_csv('./Data/finalData.csv')

    predictFuture()
    # t0 = time.time()
    # #predictFuture()
    # #predictWindow(7, 114, 120)
    # #predictDays(10)
    # # for startDay in range(100, 200):
    # #     predictDays(startDay)
    # t1 = time.time()
    # print("Time Required: " + str(t1-t0))

    #dataCleaner.fillGold()

    #missingDatesDict = dataAnalyzer.findMissingDates()
    #print(missingDatesDict)

def dataSmoothingGold():
    #goldData = btcGoldDF["Gold Price"]
    gold_smoothed = btcGoldDF[["Gold Price"]].apply(savgol_filter,  window_length=101, polyorder=2)
    btc_smoothed = btcGoldDF[["BTC Price"]].apply(savgol_filter,  window_length=101, polyorder=2)

    plt.ion()
    # plt.plot(btcGoldDF["Gold Price"])
    # plt.plot(gold_smoothed)
    plt.plot(btcGoldDF["Index"], btcGoldDF["Gold Price"])
    #plt.plot(btc_smoothed)
    plt.show()

    input()

def dataSmoothingDemo():
    # noisy data
    data = [6903.79, 6838.04, 6868.57, 6621.25, 7101.99, 7026.78, 7248.6, 7121.4, 6828.98, 6841.36, 7125.12, 7483.96, 7505.0, 7539.03, 7693.1, 7773.51, 7738.58, 8778.58, 8620.0, 8825.67, 8972.58, 8894.15, 8871.92, 9021.36, 9143.4, 9986.3, 9800.02, 9539.1, 8722.77, 8562.04, 8810.99, 9309.35, 9791.97, 9315.96, 9380.81, 9681.11, 9733.93, 9775.13, 9511.43, 9067.51, 9170.0, 9179.01, 8718.14, 8900.35, 8841.0, 9204.07, 9575.87, 9426.6, 9697.72, 9448.27, 10202.71, 9518.02, 9666.32, 9788.14, 9621.17, 9666.85, 9746.99, 9782.0, 9772.44, 9885.22, 9278.88, 9464.96, 9473.34, 9342.1, 9426.05, 9526.97, 9465.13, 9386.32, 9310.23, 9358.95, 9294.69, 9685.69, 9624.33, 9298.33, 9249.49, 9162.21, 9012.0, 9116.16, 9192.93, 9138.08, 9231.99, 9086.54, 9057.79, 9135.0, 9069.41, 9342.47, 9257.4, 9436.06, 9232.42, 9288.34, 9234.02, 9303.31, 9242.61, 9255.85, 9197.6, 9133.72, 9154.31, 9170.3, 9208.99, 9160.78, 9390.0, 9518.16, 9603.27, 9538.1, 9700.42, 9931.54, 11029.96, 10906.27, 11100.52, 11099.79, 11335.46, 11801.17, 11071.36, 11219.68, 11191.99, 11744.91, 11762.47, 11594.36, 11761.02, 11681.69, 11892.9, 11392.09, 11564.34, 11779.77, 11760.55, 11852.4, 11910.99, 12281.15, 11945.1, 11754.38]

    df = pd.DataFrame(dict(x=data))
    x_filtered = df[["x"]].apply(savgol_filter,  window_length=31, polyorder=2)

    plt.ion()
    plt.plot(data)
    plt.plot(x_filtered)
    plt.show()

    input()

def trainModel(numDataPoints):
    return regressionModels.gradientBoosting(numDataPoints)

# def predictDay(model, dayIndex):
#     model.

def predictWindow(windowSize, startDay, endDay):
    for currentDay in range(startDay, endDay):
        results = {"Price": [], "Rise Accuracy": [], "Fall Accuracy": []}

        model, predictedNextDay = trainModel(startDay)

        print(predictedNextDay[0], btcGoldDF["Gold Price"][currentDay+1])

        for i in range(1, windowSize+1):
            model = regressionModels.retrainModel(model, currentDay+i)
            predictedNextDay = regressionModels.predictDay(model, currentDay+i)

            print(predictedNextDay[0], btcGoldDF["Gold Price"][currentDay+i])

def getStartingDayAccuracy():
    for startDay in range(100, 300):
        results = {"Price": [], "Rise Accuracy": [], "Fall Accuracy": []}
        for trainingDays in range(startDay, len(btcGoldDF)-1):
            prediction = regressionModels.DecisionTree(trainingDays)

def predictFuture():
    myWallet = wallet.Wallet()
    for startDay in range(10, len(btcGoldDF)-1):
        for product in ["BTC", "Gold"]:
            regressionModels.PREDICTION = product + ' Price'
            regressionModels.DATA = [product + 'DaysSinceRise', product + 'DaysSinceFall']
            predictionDF = pd.DataFrame(columns=['Price', 'Rise', 'Fall'])

            regressionModels.setRiseFallDays(startDay)
            model = regressionModels.DecisionTree(startDay)
            for trainingDays in range(startDay+1, len(btcGoldDF)-1):
                predictionDict = {'Price': [], 'Rise': [], 'Fall': []}
                spike = False
                rise = 0
                fall = 0

                model = regressionModels.retrainModel(model, trainingDays)
                prediction = regressionModels.predictDay(model, trainingDays)

                regressionModels.addRiseFallDays(trainingDays, regressionModels.riseDays+1, regressionModels.fallDays+1)
                
                predictionDict["Price"] = prediction
                predictionDict["Rise"] = regressionModels.riseDays+1
                predictionDict["Fall"] = regressionModels.fallDays+1
                predictionDF = pd.concat([predictionDF, pd.DataFrame(predictionDict)])

                # TODO - check if rise or fall, distinguish which, get index of spike, break loop
                try:
                    value, index = findNextTopOfSpike(predictionDF["Price"], btcGoldDF[regressionModels.PREDICTION][startDay], myWallet.fees[product])
                    spike = True
                    rise += 1
                except:
                    pass

                try:
                    value, index = findNextBottomOfSpike(predictionDF["Price"], btcGoldDF[regressionModels.PREDICTION][startDay], myWallet.fees[product])
                    spike = True
                    fall += 1
                except:
                    pass

                if spike:
                    # TODO - buy or sell
                    availableMoney = myWallet.getAvailableMoney()
                    price = round(predictionDF.iloc[index]["Price"], 2)
                    if (rise):
                        if (myWallet.wallet[product]):
                            numberOfProducts = (math.floor(myWallet.wallet[product] / price))
                            if price*numberOfProducts > myWallet.wallet[product]:
                                numberOfProducts -= 1
                            if numberOfProducts <= 0:
                                continue
                            myWallet.sell(product, price, numberOfProducts)
                            startDay += index
                            break
                    if (fall):
                        numberOfProducts = (math.floor(availableMoney / price))
                        if price*numberOfProducts > availableMoney:
                            numberOfProducts -= 1
                        if numberOfProducts <= 0:
                            continue
                        myWallet.buy(product, price, numberOfProducts)
                        startDay += index
                        break

    print(myWallet)


def getRiseFall(previousPrice, currentPrice):
    if previousPrice > currentPrice:
        return "Fell"
    elif previousPrice < currentPrice:
        return "Rose"
    else:
        return "Stayed" 

def predictPurchase(df, day):
    btc_transactionFee = 0.02
    gold_transactionFee = 0.01
    lastTrainingDayPrice = df[day]
    btc_prediction = regressionModels.MLPNN(day, 'BTC Price')
    gold_prediction = regressionModels.MLPNN(day, 'Gold Price')

    btc_bestNextBestValue = findNextTopOfSpike(btc_prediction, lastTrainingDayPrice, btc_transactionFee)    
    btc_bestNextWorstValue = findNextBottomOfSpike(btc_prediction, lastTrainingDayPrice, btc_transactionFee)

    gold_bestNextBestValue = findNextTopOfSpike(gold_prediction, lastTrainingDayPrice, gold_transactionFee)    
    gold_bestNextWorstValue = findNextBottomOfSpike(gold_prediction, lastTrainingDayPrice, gold_transactionFee)

    btc_gains = (lastTrainingDayPrice - btc_bestNextBestValue)
    gold_gains = (lastTrainingDayPrice - gold_bestNextBestValue)

    btc_profit = btc_gains - (btc_gains * 0.02)
    gold_profit = gold_gains - (gold_gains * 0.01)

def findNextBottomOfSpike(prediction, startDayPrice, fee):
    lowIndex = 0
    highestValue = startDayPrice
    lowestValue = startDayPrice
    for index in range(len(prediction)):
        p = prediction.iloc[index]
        if p < lowestValue:
            lowestValue = p
            lowIndex = index
        elif (p > lowestValue and highestValue - p  > (p * fee)):
            return lowestValue, lowIndex
        
        if (p > highestValue):
            highestValue = p

def findNextTopOfSpike(prediction, startDayPrice, fee):
    highIndex = 0
    highestValue = startDayPrice
    lowestValue = startDayPrice
    for index in range(len(prediction)):
        p = prediction.iloc[index]
        if (p > highestValue):
            highestValue = p
            highIndex = index
        elif (p < highestValue and p - lowestValue > (p * fee)):
            return highestValue, highIndex
        
        if p < lowestValue:
            lowestValue = p

main()