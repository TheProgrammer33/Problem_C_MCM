import pandas as pd
import time
from multiprocessing import Process

import dataAnalyzer, dataCleaner
import regressionModels
import classificationModels
import priceEffect

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

    # resultDF = pd.DataFrame(results)
    # resultDF.to_csv('./Data/DecisionTreeBTC/trainingResults' + str(startDay) +'.csv', index=False, columns=["Training Days", "Prediction", "Actual", "Accurate"])

    summedPredictions = 0
    for accurate in results["Accurate"]:
        summedPredictions += accurate * 100
    
    accuracy = summedPredictions / len(results["Accurate"])
    # outfile = open('./Data/DecisionTreeBTC/trainingResults' + str(startDay) + '.csv', "a")
    # outfile.write(str(accuracy))
    # outfile.close()

    if (accuracy < 50):
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

    dataCleaner.combineCSVs()
    # priceEffect.setPriceEffectToFile()

    global btcGoldDF
    btcGoldDF = pd.read_csv('./Data/finalData.csv')

    t0 = time.time()
    predictFuture()
    #predictWindow(7, 114, 120)
    #predictDays(10)
    # for startDay in range(100, 200):
    #     predictDays(startDay)
    t1 = time.time()
    print("Time Required: " + str(t1-t0))

    #dataCleaner.fillGold()

    #missingDatesDict = dataAnalyzer.findMissingDates()
    #print(missingDatesDict)

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

def predictFuture():
    for startDay in range(100, 300):
        results = {"Price": [], "Rise Accuracy": [], "Fall Accuracy": []}
        for trainingDays in range(startDay, len(btcGoldDF)-1):
            prediction = regressionModels.DecisionTree(trainingDays)

            risePrice, riseIndex = findNextTopOfSpike(prediction, btcGoldDF["Gold Price"][trainingDays], 0.02)
            fallPrice, fallIndex = findNextBottomOfSpike(prediction, btcGoldDF["Gold Price"][trainingDays], 0.02)

            previousDay = btcGoldDF["Gold Price"][trainingDays + riseIndex - 1]
            actualRiseDay = getRiseFall(previousDay, btcGoldDF["Gold Price"][trainingDays + riseIndex])
            actualFallDay = getRiseFall(previousDay, btcGoldDF["Gold Price"][trainingDays + fallIndex])
            risePrediction = getRiseFall(previousDay, risePrice)
            fallPrediction = getRiseFall(previousDay, fallPrice)

            results["Price"].append(btcGoldDF["Gold Price"][predictDays])
            results["Rise Accuracy"].append(1 if risePrediction == actualRiseDay else 0)
            results["Fall Accuracy"].append(1 if fallPrediction == actualFallDay else 0)
            
            for accuracyType in ["Rise Accuracy", "Fall Accuracy"]:
                summedPredictions = 0
                for accurate in results[accuracyType]:
                    summedPredictions += accurate * 100
                
                
                accuracy = summedPredictions / len(results[accuracyType])

                if (accuracy > 50):
                    resultDF = pd.DataFrame(results)
                    resultDF.to_csv('./NeuralNetworkResults/trainingResults' + str(trainingDays) +'.csv',
                        index=False, columns=["Price", "Rise Accuracy", "Fall Accuracy"])

                    accuracy = summedPredictions / len(results[accuracyType])
                    outfile = open('./NeuralNetworkResults/trainingResults' + str(trainingDays) + '.csv', "a")
                    outfile.write(str(accuracy))
                    outfile.close()
                else:
                    outfile = open('./NeuralNetworkResults/badTrainingResults.csv', "a")
                    outfile.write(str(trainingDays) + ": " + str(accuracy) + "\n")
                    outfile.close()


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

def findNextBottomOfSpike(prediction, startDay, fee):
    heighestValue = startDay
    lowestValue = startDay
    for p in prediction:
        if p < lowestValue:
            lowestValue = p
        elif (p > lowestValue and p - heighestValue > (p * fee)):
            return lowestValue, prediction.index(p)
        
        if (p > heighestValue):
            heighestValue = p

def findNextTopOfSpike(prediction, startDay, fee):
    heighestValue = startDay
    lowestValue = startDay
    for p in prediction:
        if (p > heighestValue):
            heighestValue = p
        elif (p < heighestValue and lowestValue - p > (p * fee)):
            return heighestValue, prediction.index(p)
        
        if p < lowestValue:
            lowestValue = p


main()