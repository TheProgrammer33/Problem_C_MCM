import dataAnalyzer
import classificationModels

def main():
    print("Starting...")

    classificationModels.combineCSVs()
    #missingDatesDict = dataAnalyzer.findMissingDates()
    #print(missingDatesDict)

main()