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

    t0 = time.time()
    #automateClassifierTester()
    btcGoldDF = pd.read_csv('./Data/finalData.csv')
    for trainingDays in range(10, len(btcGoldDF)-11):
        lastTrainingDayPrice = btcGoldDF["Gold Price"][trainingDays]
        predictionForNextDay = regressionModels.DecisionTree(trainingDays)[0]
        actualPrice = btcGoldDF["Gold Price"][trainingDays+1]
        print("Prediction: " + getRiseFall(lastTrainingDayPrice, predictionForNextDay))
        print("Actual: " + getRiseFall(lastTrainingDayPrice, actualPrice))
    t1 = time.time()
    print("Time Required: " + str(t1-t0))

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