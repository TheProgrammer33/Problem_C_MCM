import dataAnalyzer

def main():
    print("Starting...")

    missingDatesDict = dataAnalyzer.findMissingDates()
    print(missingDatesDict)

main()