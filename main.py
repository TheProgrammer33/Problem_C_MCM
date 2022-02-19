import pandas as pd
import time

import dataAnalyzer
import classificationModels
import priceEffect

def automateClassifierTester():
    outputList = []

    classifiers = [classificationModels.naiveBayes, classificationModels.logisticRegression, classificationModels.decisionTree, classificationModels.randomForest]

    for i in range(10, 100):
        for classifier in classifiers:
            outputList.append(classificationModels.classifierCaller(classifier, i))
            
    df = pd.DataFrame(outputList, columns=['Number of Data Points', 'Classifier Name', 'Model Accuracy'])

    df.to_csv('./Data/Classifiers.csv', index=False)

def main():
    print("Starting...")

    t0 = time.time()
    automateClassifierTester()
    t1 = time.time()
    print("Time Required: " + str(t1-t0))
    #classificationModels.fillGold()
    #classificationModels.combineCSVs()
    
    #priceEffect.setPriceEffectToFile()

    #missingDatesDict = dataAnalyzer.findMissingDates()
    #print(missingDatesDict)

main()