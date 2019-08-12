import pandas as pd
import csv

matches = pd.read_csv('/home/joshua/PycharmProjects/dataCollector/matches', usecols=[0], names=['match'])

id = 0
count = 0
limit = 10000
matchCurr = []
matchWrite = []
for i in matches['match']:
    matchCurr.append(i)
i=0
while i < len(matchCurr):
    if count < limit:
        matchWrite.append(matchCurr[i])
        count += 1
        i += 1
    else:
        count = 0
        df = pd.DataFrame(matchWrite)
        df.to_csv(str(id), index=False)
        matchWrite.clear()
        id += 1

print("file created")