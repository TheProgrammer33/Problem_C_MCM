import pandas as pd
bitCoinExchange = pd.read_csv("Data\BCHAIN-MKPRU.csv")
goldExchange = pd.read_csv("Data\LBMA-GOLD.csv")

def findMissingDates():
    missingDates = {}
    previousDate = goldExchange["Date"][0]
    for date in goldExchange["Date"][1:]:
        missingDatesList = findDateGap(previousDate, date)
        if (missingDatesList):
            for missingDate in missingDatesList:
                try:
                    missingDates[missingDate] += 1
                except:
                    missingDates[missingDate] = 1

        previousDate = date
    return missingDates

def findDateGap(previousDate, currentDate):
    missingDates = []
    previousDay = int(getDay(previousDate))
    currentDay = int(getDay(currentDate))
    gap = currentDay - previousDay
    if (gap < 0):
        missingDates = getDatesDifferentMonths(previousDate, currentDate)
    elif (gap > 1):
        missingDates = []
        for i in range(previousDay+1, currentDay):
            missingDates.append(getMonth(previousDate) + "/" + str(i))

    return missingDates

def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]

def getDay(date):
    separatorIndexes = findOccurrences(date, "/")
    return date[int(separatorIndexes[0])+1:int(separatorIndexes[1])]

def getMonth(date):
    separatorIndexes = findOccurrences(date, "/")
    return date[:separatorIndexes[0]]

def getYear(date):
    separatorIndexes = findOccurrences(date, "/")
    return date[separatorIndexes[1]+1:]

def getDatesDifferentMonths(previousDate, currentDate):
    missingDates = []
    for i in range(int(getDay(previousDate)), 32):
        missingDates.append(getMonth(previousDate) + "/" + str(i))
    for i in range(1, int(getDay(currentDate))):
        missingDates.append(getMonth(currentDate) + "/" + str(i))