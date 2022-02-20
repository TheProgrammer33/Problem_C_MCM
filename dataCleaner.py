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

    df.to_csv('./Data/finalData.csv', index=False)

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
    previous_btc = df["BTC Price"][0]
    previous_gold = df["Gold Price"][0]

    for day in range(len(df["BTC Price"][1:])):
        btc_price = df["BTC Price"][day]
        gold_price = df["Gold Price"][day]
        if (btc_price > previous_btc):
            riseFallDict["BTCDaysSinceFall"].append(riseFallDict["BTCDaysSinceFall"][-1])
            riseFallDict["BTCDaysSinceRise"].append(0)
        elif (btc_price < previous_btc):
            riseFallDict["BTCDaysSinceFall"].append(0)
            riseFallDict["BTCDaysSinceRise"].append(riseFallDict["BTCDaysSinceRise"][-1] + 1)
        else:
            riseFallDict["BTCDaysSinceFall"].append(riseFallDict["BTCDaysSinceFall"][-1] + 1)
            riseFallDict["BTCDaysSinceRise"].append(riseFallDict["BTCDaysSinceRise"][-1] + 1)

        if (gold_price > previous_gold):
            riseFallDict["GoldDaysSinceFall"].append(riseFallDict["GoldDaysSinceFall"][-1])
            riseFallDict["GoldDaysSinceRise"].append(0)
        elif (gold_price < previous_gold):
            riseFallDict["GoldDaysSinceFall"].append(0)
            riseFallDict["GoldDaysSinceRise"].append(riseFallDict["GoldDaysSinceRise"][-1] + 1)
        else:
            riseFallDict["GoldDaysSinceFall"].append(riseFallDict["GoldDaysSinceFall"][-1] + 1)
            riseFallDict["GoldDaysSinceRise"].append(riseFallDict["GoldDaysSinceRise"][-1] + 1)

        previous_btc = btc_price
        previous_gold = gold_price

            