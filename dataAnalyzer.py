from calendar import leapdays
from tracemalloc import start
import pandas as pd
bitCoinExchange = pd.read_csv("./Data/BCHAIN-MKPRU.csv")
goldExchange = pd.read_csv("./Data/LBMA-GOLD.csv")

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
            missingDates.append(getMonth(previousDate) + "/" + str(i) + "/" + getYear(previousDate))

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

    months = [2, 4, 6, 9, 11]
    monthsDayCounts = [28, 30, 30, 30, 30]
    leapDays = 0

    if (int(getYear(previousDate)) % 4 == 0 and (int(getMonth(previousDate))) == 2):
        leapDays = 1

    if (months.count(int(getMonth(previousDate))) > 0):
        for i in range(int(getDay(previousDate))+1, monthsDayCounts[months.index(int(getMonth(previousDate)))] + 1 + leapDays):
            missingDates.append(getMonth(previousDate) + "/" + str(i) + "/" + getYear(previousDate))
    else:
        for i in range(int(getDay(previousDate))+1, 32):
            missingDates.append(getMonth(previousDate) + "/" + str(i) + "/" + getYear(previousDate))

    for i in range(1, int(getDay(currentDate))):
        missingDates.append(getMonth(currentDate) + "/" + str(i) + "/" + getYear(currentDate))

    return missingDates

def getDFPosition(date):
    startDate = '9/11/16'

    position = getDaysBetweenDates(startDate, date)

    return position

def getDaysBetweenDates(startDate, endDate):
    startDay = int(getDay(startDate))
    startMonth = (int(getMonth(startDate)))
    startYear = int(getYear(startDate))

    endDay = int(getDay(endDate))
    endMonth = (int(getMonth(endDate)))
    endYear = int(getYear(endDate))

    days = 0

    days += getDaysBetweenMonths(startMonth, endMonth, startYear, endYear)
    days += getDaysBetweenDays(startDay, endDay, endMonth)

    return days

    

def getDaysBetweenMonths(startMonth, endMonth, startYear, endYear):
    days = 0
    leapdays = 0

    if endMonth - startMonth < 0:
        for i in range(0, 12 - endMonth):
            days += getDaysFromMonth(i+endMonth)
        
        for i in range(0, startMonth):
            days += getDaysFromMonth(i)

        days += (endYear-startYear)*365

    elif endMonth - startMonth > 0:
        for i in range(0, endMonth - startMonth):
            days += getDaysFromMonth(i+startMonth)
    
    return days

def getDaysBetweenDays(startDay, endDay, endMonth):
    if endDay - startDay > 0:
        return endDay - startDay
    else:
        return getDaysFromMonth(endMonth) - endDay

def getDaysFromMonth(month):
    months = [2, 4, 6, 9, 11]
    monthsDayCounts = [28, 30, 30, 30, 30]

    if months.count(month) > 0:
        return monthsDayCounts[months.index(month)]
    else:
        return 31
