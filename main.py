import pandas as pd

import dataAnalyzer
import classificationModels
import priceEffect

def automateClassifierTester():
    outputList = [[]]

    classifiers = [classificationModels.naiveBayes, classificationModels.logisticRegression, classificationModels.decisionTree, classificationModels.randomForest]

    for i in range(10, 11):
        for classifier in classifiers:
            outputList.insert(classificationModels.classifierCaller(classifier, i))

    df = pd.DataFrame(columns=['Number of Data Points', 'Classifier Name', 'Model Accuracy'], value=outputList)

    df.to_csv('./Data/Classifiers.csv')

def main():
    print("Starting...")

    #classificationModels.combineCSVs()
    
    #missingDatesDict = dataAnalyzer.findMissingDates()
    #print(missingDatesDict)

main()