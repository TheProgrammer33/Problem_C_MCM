import pandas as pd
import time
from multiprocessing import Process

import dataAnalyzer, dataCleaner
import regressionModels
import classificationModels
import wallet

import matplotlib.pyplot as plt
import math
from scipy.signal import savgol_filter

NUM_PROC = 4

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

    dataCleaner.combineCSVs()

    global btcGoldDF
    btcGoldDF = pd.read_csv('./Data/finalData.csv')

    predictFuture()

def predictFuture():
    # TODO - find best starting day
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
                    if (rise):
                        if (myWallet.wallet[product] > 0):
                            actualPrice = btcGoldDF.iloc[startDay + index][product + " Price"]
                            print("Selling " + str(myWallet.wallet[product]) + " " + product)
                            myWallet.sell(product, actualPrice)
                            startDay += index
                            break
                    if (fall):
                        actualPrice = btcGoldDF.iloc[startDay + index][product + " Price"]
                        numberOfProducts = (math.floor(availableMoney / actualPrice))
                        if actualPrice*numberOfProducts > availableMoney:
                            numberOfProducts -= 1
                        if numberOfProducts <= 0:
                            continue
                        print("Buying " + str(numberOfProducts) + " " + product)
                        myWallet.buy(product, actualPrice, numberOfProducts)
                        startDay += index
                        break

    print(myWallet.wallet)

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