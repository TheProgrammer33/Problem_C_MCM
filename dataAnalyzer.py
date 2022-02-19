from calendar import leapdays
from tracemalloc import start
import pandas as pd
bitCoinExchange = pd.read_csv("./Data/BCHAIN-MKPRU.csv")
goldExchange = pd.read_csv("./Data/LBMA-GOLD.csv")

def findMissingDates():
    missingDates = []
    previousDate = goldExchange["Date"][0]
    for date in goldExchange["Date"][1:]:
        missingDates += findDateGap(previousDate, date)
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

    if (startMonth != endMonth or (startDay > endDay and endYear > startYear)):
        days += getDaysBetweenMonths(startMonth, endMonth, startDay, endDay)
    else:
        days += getDaysBetweenDays(startDay, endDay)
    
    days += getDaysBetweenYears(startYear, endYear, startMonth, endMonth, startDay, endDay)

    return days

def getDaysBetweenMonths(startMonth, endMonth, startDay, endDay):
    days = 0

    if endMonth - startMonth <= 0:
        for month in range(startMonth, 13):
            if (month == startMonth):
                days += getDaysInMonth(month) - startDay
            else:
                days += getDaysInMonth(month)

        for i in range(1, endMonth):
            days += getDaysInMonth(i)
    elif endMonth - startMonth > 0:
        for month in range(startMonth, endMonth):
            if (month == startMonth):
                days += getDaysInMonth(month) - startDay
            else:
                days += getDaysInMonth(month)
    
    days += endDay
    
    return days

def getDaysBetweenDays(startDay, endDay):
    if endDay - startDay > 0:
        return endDay - startDay
    return 0 

def getDaysBetweenYears(startYear, endYear, startMonth, endMonth, startDay, endDay):
    days = 0
    numYearsApart = endYear - startYear
    if (numYearsApart > 0):
        numMonthsApart = endMonth - startMonth
        if (numMonthsApart >= 0):
            if (endDay - startDay >= 0):
                days += (endYear-startYear)*365
            elif (numMonthsApart > 0 and not numYearsApart < 1):
                days += (endYear-startYear)*365
            elif (numYearsApart > 1):
                days += (endYear-startYear-1)*365
        elif (numYearsApart > 1):
            days += (endYear-startYear-1)*365

    return days

def getDaysInMonth(month):
    months = [2, 4, 6, 9, 11]
    monthsDayCounts = [28, 30, 30, 30, 30]

    if months.count(month) > 0:
        return monthsDayCounts[months.index(month)]
    else:
        return 31

def getMissingPrices():
    missingPriceDates = []
    for priceIndex in range(len(goldExchange["USD (PM)"])):
        if (goldExchange["USD (PM)"][priceIndex]):
            missingPriceDates.append(goldExchange["Date"][priceIndex])
    return missingPriceDates
