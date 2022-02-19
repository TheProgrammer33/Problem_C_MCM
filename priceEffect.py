import pandas as pd

def setPriceEffectToFile():
    datastream = pd.read_csv("./Data/finalData.csv")

    outfile = open("./Data/finalData.csv", "w")
    outfile.write("Index,Date,Gold Price,BTC Price,GoldDelta,BitcoinDelta,GoldPriceEffect,BitcoinPriceEffect\n")

    prevValGold = datastream["Gold Price"][0]
    prevValBTC = datastream["BTC Price"][0]

    for i in range(len(datastream["Date"])):
        outfile.write(str(i) + "," + datastream["Date"][i] + ",")
        curValGold = datastream["Gold Price"][i]
        curValBTC = datastream["BTC Price"][i]
        outfile.write(str(curValGold) + "," + str(curValBTC) + ",")
        deltaGold = round(curValGold - prevValGold, 4)
        deltaBTC = round(curValBTC - prevValBTC, 4)
        
        outfile.write(str(deltaGold) + "," + str(deltaBTC) + ",")

        if (deltaGold > 0):
            outfile.write("1,")
        elif (deltaGold < 0):
            outfile.write("0,")
        else:
            outfile.write("2,")
        prevValGold = curValGold

        if (deltaBTC > 0):
            outfile.write("1")
        elif (deltaBTC < 0):
            outfile.write("0")
        else:
            outfile.write("2")
        prevValBTC = curValBTC

        outfile.write("\n")