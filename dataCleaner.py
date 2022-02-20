import pandas as pd
import numpy as np
import time
from datetime import date as Date

import dataAnalyzer

def combineCSVs():
    goldDF = pd.read_csv('./Data/newGold.csv')
    btcDF = pd.read_csv('./Data/BCHAIN-MKPRU.csv')

    df = goldDF.join(btcDF['BTC Price'])
    # df = df.join(getDatesDataFrame(df)["Unix Time"])
    df = df.join(getDaysSinceRiseAndFall(df))

    df.to_csv('./Data/finalData.csv', index=True)

def insert_row(idx, df, df_insert):
    dfA = df.iloc[:idx]
    dfB = df.iloc[idx:]

    df = dfA.append(df_insert).append(dfB).reset_index(drop = True)

    return df

def fillGold():
    goldDF = pd.read_csv('./Data/fixedGold.csv')

    missingDates = dataAnalyzer.findMissingDates()

    for date in missingDates:
        positionInDF = dataAnalyzer.getDFPosition(date)

        goldDF = insert_row(positionInDF-1, goldDF,
            pd.DataFrame(np.array([[date, 
            goldDF['USD (PM)'][positionInDF-1]]]),
            columns=['Date', 'USD (PM)']))
        #goldDF.loc[positionInDF] = [date, goldDF[positionInDF-1]]

    goldDF.to_csv('./Data/newGold.csv', index=False)

def fixGold():
    goldDF = pd.read_csv('./Data/LBMA-GOLD.csv')

    positions, dates = dataAnalyzer.getMissingPriceDates(goldDF)

    for i in range(len(positions)):
        goldDF.loc[positions[i]] = dates[i], goldDF['USD (PM)'][positions[i]-1]

    goldDF.to_csv('./Data/fixedGold.csv', index=False)

def getDatesDataFrame(df):
    datesDF = df['Date']
    unixTimeList = {"Unix Time": []}

    # TODO - make date object and set a dataframe with the dates as integers
    for date in datesDF:
        dateObject = Date(2000 + int(dataAnalyzer.getYear(date)), int(dataAnalyzer.getMonth(date)), int(dataAnalyzer.getDay(date)))

        unixTimeList['Unix Time'].append(time.mktime(dateObject.timetuple()))

    return pd.DataFrame(unixTimeList)

def getDaysSinceRiseAndFall(df):
    riseFallDict = {"BTCDaysSinceRise": [0], "BTCDaysSinceFall": [0], "GoldDaysSinceRise": [0], "GoldDaysSinceFall": [0], }
    transactionFee = {"BTC": 0.02, "Gold": 0.01}

    for t in ["BTC", "Gold"]:
        highestValueIndex = 0
        lowestValueIndex = 0
        currentDF = df[t + " Price"]
        for day in range(len(df[t + " Price"][1:])):
            price = currentDF[day]
            if price < currentDF[lowestValueIndex]:
                riseFallDict[t + "DaysSinceFall"].append(riseFallDict[t + "DaysSinceFall"][-1] + 1)
                lowestValueIndex = day
            elif (price > currentDF[lowestValueIndex] and price - currentDF[highestValueIndex] > (price * (transactionFee[t]))):
                # Low Spike
                riseFallDict[t + "DaysSinceFall"].append(0)
                riseFallDict[t + "DaysSinceFall"][lowestValueIndex+1:] = replaceValueInList(riseFallDict[t + "DaysSinceFall"][lowestValueIndex+1:])
                riseFallDict[t + "DaysSinceFall"][lowestValueIndex] = 0
            elif (price >= currentDF[lowestValueIndex]):
                riseFallDict[t + "DaysSinceFall"].append(riseFallDict[t + "DaysSinceFall"][-1] + 1)

            if (price > currentDF[highestValueIndex]):
                riseFallDict[t + "DaysSinceRise"].append(riseFallDict[t + "DaysSinceRise"][-1] + 1)
                highestValueIndex = day
            elif (price < currentDF[highestValueIndex] and currentDF[lowestValueIndex] - price > (price * transactionFee[t])):
                # High Spike
                riseFallDict[t + "DaysSinceRise"].append(0)
                riseFallDict[t + "DaysSinceFall"][highestValueIndex+1:] = replaceValueInList(riseFallDict[t + "DaysSinceRise"][highestValueIndex+1:])
                riseFallDict[t + "DaysSinceFall"][highestValueIndex] = 0
            elif (price <= currentDF[highestValueIndex]):
                riseFallDict[t + "DaysSinceRise"].append(riseFallDict[t + "DaysSinceRise"][-1] + 1)

    return pd.DataFrame(riseFallDict)
    
def replaceValueInList(l):
    newl = []
    for i in range(len(l)):
        newl.append(i+1)
    return newl
