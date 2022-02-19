import pandas as pd
import time

import dataAnalyzer, dataCleaner
import regressionModels
import classificationModels
import priceEffect

def main():
    print("Starting...")

    dataCleaner.combineCSVs()
    priceEffect.setPriceEffectToFile()

    outputPredictions = []
    t0 = time.time()
    btcGoldDF = pd.read_csv('./Data/finalData.csv')
    results = {"Training Days": [], "Prediction": [], "Actual": [], "Accurate": []}

    for trainingDays in range(10, len(btcGoldDF)-11):
        lastTrainingDayPrice = btcGoldDF["Gold Price"][trainingDays]
        predictionForNextDay = getRiseFall(lastTrainingDayPrice, regressionModels.DecisionTree(trainingDays)[0])
        actualNextDay = getRiseFall(lastTrainingDayPrice, btcGoldDF["Gold Price"][trainingDays+1])

        results["Training Days"].append(lastTrainingDayPrice)
        results["Prediction"].append(predictionForNextDay)
        results["Actual"].append(actualNextDay)
        results["Accurate"].append(1 if predictionForNextDay == actualNextDay else 0)

        outputPredictions.append([predictionForNextDay, actualNextDay])

    resultDF = pd.DataFrame(results)
    resultDF.to_csv('./Data/trainingResults.csv', index=False, columns=["Training Days", "Prediction", "Actual", "Accurate"])

    t1 = time.time()
    print("Time Required: " + str(t1-t0))

    summedPredictions = 0

    for output in outputPredictions:
        if output[0] == output[1]:
            summedPredictions += 100
        else:
            summedPredictions += 0
    
    accuracy = summedPredictions / len(outputPredictions)

    print("Final accuracy: " + str(accuracy) + "%")

    #dataCleaner.fillGold()

    #missingDatesDict = dataAnalyzer.findMissingDates()
    #print(missingDatesDict)

def getRiseFall(previousPrice, currentPrice):
    if previousPrice > currentPrice:
        return "Fell"
    elif previousPrice < currentPrice:
        return "Rose"
    else:
        return "Stayed" 

main()