import pandas as pd
import numpy as np
import time
from datetime import date as Date

import dataAnalyzer

def combineCSVs():
    goldDF = pd.read_csv('./Data/newGold.csv')
    btcDF = pd.read_csv('./Data/BCHAIN-MKPRU.csv')

    df = goldDF.join(btcDF['BTC Price'])
    df = df.join(getDatesDataFrame(df)["Unix Time"])

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