import dataAnalyzer
import classificationModels
import priceEffect

def main():
    print("Starting...")

    priceEffect.setPriceEffectToFile()
    # classificationModels.combineCSVs()
    #missingDatesDict = dataAnalyzer.findMissingDates()
    #print(missingDatesDict)

main()