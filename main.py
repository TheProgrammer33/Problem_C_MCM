import pandas as pd
import time
from multiprocessing import Process

import dataAnalyzer, dataCleaner
import regressionModels
import classificationModels
import priceEffect

NUM_PROC = 4

btcGoldDF = pd.read_csv('./Data/finalData.csv')

def predictDays(bs, startDay):
    results = {"Training Days": [], "Prediction": [], "Actual": [], "Accurate": []}

    for trainingDays in range(startDay, len(btcGoldDF)-1):
        lastTrainingDayPrice = btcGoldDF["BTC Price"][trainingDays]
        predictionForNextDay = getRiseFall(lastTrainingDayPrice, regressionModels.DecisionTree(trainingDays)[0])
        actualNextDay = getRiseFall(lastTrainingDayPrice, btcGoldDF["BTC Price"][trainingDays+1])

        results["Training Days"].append(lastTrainingDayPrice)
        results["Prediction"].append(predictionForNextDay)
        results["Actual"].append(actualNextDay)
        results["Accurate"].append(1 if predictionForNextDay == actualNextDay else 0)

    resultDF = pd.DataFrame(results)
    resultDF.to_csv('./Data/DecisionTreeBTC/trainingResults' + str(startDay) +'.csv', index=False, columns=["Training Days", "Prediction", "Actual", "Accurate"])

    summedPredictions = 0
    for accurate in results["Accurate"]:
        summedPredictions += accurate * 100
    
    accuracy = summedPredictions / len(results["Accurate"])
    outfile = open('./Data/DecisionTreeBTC/trainingResults' + str(startDay) + '.csv', "a")
    outfile.write(str(accuracy))
    outfile.close()

def train():
    # Change range values (start day, lastStartDay)
    for startDay in range(15, 300, NUM_PROC):
        jobs = []

        for i in range(NUM_PROC):
            process = Process(
                target=predictDays, 
                args=([], startDay+i)
            )
            jobs.append(process)

        for j in jobs:
            j.start()

        for j in jobs:
            j.join()


def main():
    print("Starting...")

    dataCleaner.combineCSVs()
    priceEffect.setPriceEffectToFile()

    t0 = time.time()
    train()
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