import pandas as pd

# Currently just for Bitcoin

bitcoinRd = pd.read_csv("./Data/BCHAIN-MKPRU.csv")

f = open("output_test.txt", "w")
f.write("Date\t-- Value  -- Delta(B) -- PE(B)\n")

prevVal = bitcoinRd["Value"][0]
f.write(bitcoinRd["Date"][0] + " -- " + str(prevVal) + " -- null -- -1\n")

count = 1

for date in bitcoinRd["Date"][1:]:
    f.write(date + " -- ")
    curVal = bitcoinRd["Value"][count]
    f.write(str(curVal) + " -- ")
    delta = round(curVal - prevVal, 4)
    
    f.write(str(delta) + " -- ")

    if (delta > 0):
        f.write("1")
    elif (delta < 0):
        f.write("0")
    prevVal = curVal
    count+=1
    f.write("\n")