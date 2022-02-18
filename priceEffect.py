import pandas as pd

datastream = pd.read_csv("./Data/finalData.csv")

outfile = open("./Data/finaldataPE.csv", "w")
outfile.write("Date,USD (PM),BTC Price,Delta(G),Delta(B),PE(G),PE(B)\n")

prevValGold = datastream["USD (PM)"][0]
prevValBTC = datastream["BTC Price"][0]
outfile.write(datastream["Date"][0] + "," + str(prevValGold) + "," + str(prevValBTC) + ",null,-1,null,-1\n")

count = 1

for date in datastream["Date"][1:]:
    outfile.write(date + ",")
    curValGold = datastream["USD (PM)"][count]
    curValBTC = datastream["BTC Price"][count]
    outfile.write(str(curValGold) + "," + str(curValBTC) + ",")
    deltaGold = round(curValGold - prevValGold, 4)
    deltaBTC = round(curValBTC - prevValBTC, 4)
    
    outfile.write(str(deltaGold) + "," + str(deltaBTC) + ",")

    if (deltaGold > 0):
        outfile.write("1,")
    elif (deltaGold < 0):
        outfile.write("0,")
    prevValGold = curValGold

    if (deltaBTC > 0):
        outfile.write("1")
    elif (deltaBTC < 0):
        outfile.write("0")
    prevValBTC = curValBTC

    count+=1
    outfile.write("\n")