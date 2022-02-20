import pandas as pd
import numpy as np
from datetime import datetime

import dataAnalyzer

def combineCSVs():
    goldDF = pd.read_csv('./Data/newGold.csv')
    btcDF = pd.read_csv('./Data/BCHAIN-MKPRU.csv')

    df = goldDF.join(btcDF['BTC Price'])
    df = df.join(getDatesDataFrame(df))

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

    # TODO - make date object and set a dataframe with the dates as integers
    for date in datesDF:
        dateObject = datetime.date(int("20" + dataAnalyzer.getYear(date)), int(dataAnalyzer.getMonth(date)), int(dataAnalyzer.getDay(date)))



    return datesDF