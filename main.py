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

    # Change range values (start day, lastStartDay)
    for startDay in range(10, 1500):
        for trainingDays in range(startDay, len(btcGoldDF)-1):
            lastTrainingDayPrice = btcGoldDF["Gold Price"][trainingDays]
            predictionForNextDay = getRiseFall(lastTrainingDayPrice, regressionModels.MLPNN(trainingDays)[0])
            actualNextDay = getRiseFall(lastTrainingDayPrice, btcGoldDF["Gold Price"][trainingDays+1])

            results["Training Days"].append(lastTrainingDayPrice)
            results["Prediction"].append(predictionForNextDay)
            results["Actual"].append(actualNextDay)
            results["Accurate"].append(1 if predictionForNextDay == actualNextDay else 0)

        resultDF = pd.DataFrame(results)
        resultDF.to_csv('./NeuralNetworkResults/trainingResults' + str(startDay) +'.csv', index=False, columns=["Training Days", "Prediction", "Actual", "Accurate"])

        summedPredictions = 0
        for accurate in results["Accurate"]:
            summedPredictions += accurate * 100
        
        accuracy = summedPredictions / len(results["Accurate"])
        outfile = open('./NeuralNetworkResults/trainingResults' + str(startDay) + '.csv', "a")
        outfile.write(str(accuracy))
        outfile.close()


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