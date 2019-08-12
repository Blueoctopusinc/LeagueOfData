import pandas as pd
import math
import random
import numpy as np
import collections
goldData = pd.read_csv('/home/joshua/PycharmProjects/dataCollector/goldChampData.csv')
myData = pd.read_csv('/home/joshua/PycharmProjects/dataCollector/data_set_large/dataset_1')
checkData = myData.to_dict('records')
dfCheck = pd.DataFrame(checkData)
dfCheck.to_csv("check")
adc = eval(myData.get('Adc')[0])
match_count = 0

records = len(myData.index)
x = 0
inval_count = 0
i = 0
samples = []
samplesaverages = []
noneSamples = 0
y = 0
recordskip = []


def dataset2array(data, index, arr, height, width, row):
    posRow = index * 14
    np.put(arr, [int(width * row + posRow)], data['champion'])
    np.put(arr, [int(width * row + (posRow + 1))], data['kills'])
    np.put(arr, [int(width * row + (posRow + 2))], data['deaths'])
    np.put(arr, [int(width * row + (posRow + 3))], data['assists'])
    np.put(arr, [int(width * row + (posRow + 4))], data['killSpree'])
    np.put(arr, [int(width * row + (posRow + 5))], data['damage'])
    np.put(arr, [int(width * row + (posRow + 6))], data['gold'])
    np.put(arr, [int(width * row + (posRow + 7))], data['cs'])
    np.put(arr, [int(width * row + (posRow + 8))], data['teamJungle'])
    np.put(arr, [int(width * row + (posRow + 9))], data['enemyJungle'])
    np.put(arr, [int(width * row + (posRow + 10))], data['damageTaken'])
    np.put(arr, [int(width * row + (posRow + 11))], data['totalHeal'])
    np.put(arr, [int(width * row + (posRow + 12))], data['playerWinrateLast25'])
    np.put(arr, [int(width * row + (posRow + 13))], data['championGames'])
    return

while y < records:
    if pd.isnull(myData.get('Adc')[y]) or pd.isnull(myData.get('Top')[y]) or pd.isnull(myData.get('Middle')[y]) or pd.isnull(myData.get('Jungle')[y]) or pd.isnull(myData.get('Support')[y]):
        if y % 2 == 0:
            recordskip.append(y)
            recordskip.append(y+1)
            y+=2
        else:
            recordskip.append(y)
            recordskip.append(y-1)
            y+=1
    else:
        y+=1


while x < records:
    #print(i)
    if x not in recordskip:
        team = {}
        teamaverages = {}
        test = myData.get('Jungle')[x]
        adc = eval(myData.get('Adc')[x])
        top = eval(myData.get('Top')[x])
        mid = eval(myData.get('Middle')[x])
        jung = eval(myData.get('Jungle')[x])
        sup = eval(myData.get('Support')[x])
        team['Top']=top
        team['Middle'] = mid
        team['Jungle'] = jung
        team['Support'] = sup
        team['ADC'] = adc
        team['win']=myData.get('win')[x]
        for q, y in team.items():
            if type(y) is dict:

                if y['playerWinrateLast25'] is None or y['championGames'] is None:
                    noneSamples +=1
                    champ = y['champion']

                    for i, row in goldData.iterrows():
                        if row['key'] == champ and row['role'] == q and not math.isnan(row['general.experience']):
                            team[q]['playerWinrateLast25'] = row['general.winPercent']
                            team[q]['championGames'] = round(row['general.experience'])
                            #print(team[x])
                    if team[q]['playerWinrateLast25'] is None or team[q]['championGames'] is None:
                        for i, row in goldData.iterrows():
                            if row['key'] == champ:
                                if math.isnan(row['general.experience']):
                                    team[q]['playerWinrateLast25'] = row['general.winPercent']
                                    team[q]['championGames']= random.randint(4,10)
                                else:
                                    team[q]['playerWinrateLast25'] = row['general.winPercent']
                                    team[q]['championGames'] = round(row['general.experience'])


        for q, y in team.items():
            check = False
            player = {}
            if type(y) is dict:
                player['champion'] = y['champion']
                player['playerWinrate'] = y['playerWinrateLast25']
                player['championGames'] = y['championGames']
                for i, row in goldData.iterrows():
                    if row['key'] == y['champion'] and row['role'] == q and not math.isnan(row['general.experience']):
                        check = True
                        player['position'] = row['general.overallPosition']
                        player['champwinrate'] = row['general.winPercent']
                        player['averageGames'] = row['general.experience']
                if not check:
                    for i, row in goldData.iterrows():

                        if row['key'] == y['champion']:
                            if math.isnan(row['general.experience']):
                                player['champwinrate'] = row['general.winPercent']
                                player['position'] = row['general.overallPosition']
                                player['averageGames'] = random.randint(4, 10)
                            else:
                                player['position'] = row['general.overallPosition']
                                player['champwinrate'] = row['general.winPercent']
                                player['averageGames'] = row['general.experience']
                teamaverages[q]=player


        samples.append(team)
        samplesaverages.append(teamaverages)
        x += 1
    if x in recordskip:
        x+=1
t = 0
height = int(len(samples)/2)
dataset = np.empty((height,140), dtype=object)
datasetchamp = np.empty((height,10))
datasetchampaverages = np.empty((height,60))
games = 0
labels = np.empty((height,1), dtype=int)
labelcount=0
while t < len(samples):

    featureIndex =0
    np.put(datasetchamp,[int(0+(games*10))],samples[t]['Top']['champion'])
    np.put(datasetchamp, [int(1+(games*10))], samples[t]['Middle']['champion'])
    np.put(datasetchamp, [int(2+(games*10))], samples[t]['Jungle']['champion'])
    np.put(datasetchamp, [int(3 + (games * 10))], samples[t]['Support']['champion'])
    np.put(datasetchamp, [int(4 + (games * 10))], samples[t]['ADC']['champion'])
    np.put(datasetchamp, [int(5 + (games * 10))], samples[t+1]['Top']['champion'])
    np.put(datasetchamp, [int(6 + (games * 10))], samples[t+1]['Middle']['champion'])
    np.put(datasetchamp, [int(7 + (games * 10))], samples[t+1]['Jungle']['champion'])
    np.put(datasetchamp, [int(8 + (games * 10))], samples[t+1]['Support']['champion'])
    np.put(datasetchamp, [int(9 + (games * 10))], samples[t+1]['ADC']['champion'])


    np.put(datasetchampaverages, [int(0 + (games * 60))], samplesaverages[t]['Top']['champion'])
    np.put(datasetchampaverages, [int(1 + (games * 60))], samplesaverages[t]['Top']['champwinrate'])
    np.put(datasetchampaverages, [int(2 + (games * 60))], samplesaverages[t]['Top']['position'])
    np.put(datasetchampaverages, [int(3 + (games * 60))], samplesaverages[t]['Top']['playerWinrate'])
    np.put(datasetchampaverages, [int(4 + (games * 60))], samplesaverages[t]['Top']['championGames'])
    np.put(datasetchampaverages, [int(5 + (games * 60))], samplesaverages[t]['Top']['averageGames'])


    np.put(datasetchampaverages, [int(6 + (games * 60))], samplesaverages[t]['Middle']['champion'])
    np.put(datasetchampaverages, [int(7 + (games * 60))], samplesaverages[t]['Middle']['champwinrate'])
    np.put(datasetchampaverages, [int(8 + (games * 60))], samplesaverages[t]['Middle']['position'])
    np.put(datasetchampaverages, [int(9 + (games * 60))], samplesaverages[t]['Middle']['playerWinrate'])
    np.put(datasetchampaverages, [int(10 + (games * 60))], samplesaverages[t]['Middle']['championGames'])
    np.put(datasetchampaverages, [int(11 + (games * 60))], samplesaverages[t]['Middle']['averageGames'])


    np.put(datasetchampaverages, [int(12 + (games * 60))], samplesaverages[t]['Jungle']['champion'])
    np.put(datasetchampaverages, [int(13 + (games * 60))], samplesaverages[t]['Jungle']['champwinrate'])
    np.put(datasetchampaverages, [int(14 + (games * 60))], samplesaverages[t]['Jungle']['position'])
    np.put(datasetchampaverages, [int(15 + (games * 60))], samplesaverages[t]['Jungle']['playerWinrate'])
    np.put(datasetchampaverages, [int(16 + (games * 60))], samplesaverages[t]['Jungle']['championGames'])
    np.put(datasetchampaverages, [int(17 + (games * 60))], samplesaverages[t]['Jungle']['averageGames'])


    np.put(datasetchampaverages, [int(18 + (games * 60))], samplesaverages[t]['Support']['champion'])
    np.put(datasetchampaverages, [int(19 + (games * 60))], samplesaverages[t]['Support']['champwinrate'])
    np.put(datasetchampaverages, [int(20 + (games * 60))], samplesaverages[t]['Support']['position'])
    np.put(datasetchampaverages, [int(21 + (games * 60))], samplesaverages[t]['Support']['playerWinrate'])
    np.put(datasetchampaverages, [int(22 + (games * 60))], samplesaverages[t]['Support']['championGames'])
    np.put(datasetchampaverages, [int(23 + (games * 60))], samplesaverages[t]['Support']['averageGames'])


    np.put(datasetchampaverages, [int(24 + (games * 60))], samplesaverages[t]['ADC']['champion'])
    np.put(datasetchampaverages, [int(25 + (games * 60))], samplesaverages[t]['ADC']['champwinrate'])
    np.put(datasetchampaverages, [int(26 + (games * 60))], samplesaverages[t]['ADC']['position'])
    np.put(datasetchampaverages, [int(27 + (games * 60))], samplesaverages[t]['ADC']['playerWinrate'])
    np.put(datasetchampaverages, [int(28 + (games * 60))], samplesaverages[t]['ADC']['championGames'])
    np.put(datasetchampaverages, [int(29 + (games * 60))], samplesaverages[t]['ADC']['averageGames'])


    np.put(datasetchampaverages, [int(30 + (games * 60))], samplesaverages[t+1]['Top']['champion'])
    np.put(datasetchampaverages, [int(31 + (games * 60))], samplesaverages[t+1]['Top']['champwinrate'])
    np.put(datasetchampaverages, [int(32 + (games * 60))], samplesaverages[t+1]['Top']['position'])
    np.put(datasetchampaverages, [int(33 + (games * 60))], samplesaverages[t+1]['Top']['playerWinrate'])
    np.put(datasetchampaverages, [int(34 + (games * 60))], samplesaverages[t+1]['Top']['championGames'])
    np.put(datasetchampaverages, [int(35 + (games * 60))], samplesaverages[t+1]['Top']['averageGames'])


    np.put(datasetchampaverages, [int(36 + (games * 60))], samplesaverages[t+1]['Middle']['champion'])
    np.put(datasetchampaverages, [int(37 + (games * 60))], samplesaverages[t+1]['Middle']['champwinrate'])
    np.put(datasetchampaverages, [int(38 + (games * 60))], samplesaverages[t+1]['Middle']['position'])
    np.put(datasetchampaverages, [int(39 + (games * 60))], samplesaverages[t+1]['Middle']['playerWinrate'])
    np.put(datasetchampaverages, [int(40 + (games * 60))], samplesaverages[t+1]['Middle']['championGames'])
    np.put(datasetchampaverages, [int(41 + (games * 60))], samplesaverages[t+1]['Middle']['averageGames'])


    np.put(datasetchampaverages, [int(42 + (games * 60))], samplesaverages[t+1]['Jungle']['champion'])
    np.put(datasetchampaverages, [int(43 + (games * 60))], samplesaverages[t+1]['Jungle']['champwinrate'])
    np.put(datasetchampaverages, [int(44 + (games * 60))], samplesaverages[t+1]['Jungle']['position'])
    np.put(datasetchampaverages, [int(45 + (games * 60))], samplesaverages[t+1]['Jungle']['playerWinrate'])
    np.put(datasetchampaverages, [int(46 + (games * 60))], samplesaverages[t+1]['Jungle']['championGames'])
    np.put(datasetchampaverages, [int(47 + (games * 60))], samplesaverages[t+1]['Jungle']['averageGames'])


    np.put(datasetchampaverages, [int(48 + (games * 60))], samplesaverages[t+1]['Support']['champion'])
    np.put(datasetchampaverages, [int(49 + (games * 60))], samplesaverages[t+1]['Support']['champwinrate'])
    np.put(datasetchampaverages, [int(50 + (games * 60))], samplesaverages[t+1]['Support']['position'])
    np.put(datasetchampaverages, [int(51 + (games * 60))], samplesaverages[t+1]['Support']['playerWinrate'])
    np.put(datasetchampaverages, [int(52 + (games * 60))], samplesaverages[t+1]['Support']['championGames'])
    np.put(datasetchampaverages, [int(53 + (games * 60))], samplesaverages[t+1]['Support']['averageGames'])


    np.put(datasetchampaverages, [int(54 + (games * 60))], samplesaverages[t+1]['ADC']['champion'])
    np.put(datasetchampaverages, [int(55 + (games * 60))], samplesaverages[t+1]['ADC']['champwinrate'])
    np.put(datasetchampaverages, [int(56 + (games * 60))], samplesaverages[t+1]['ADC']['position'])
    np.put(datasetchampaverages, [int(57 + (games * 60))], samplesaverages[t+1]['ADC']['playerWinrate'])
    np.put(datasetchampaverages, [int(58 + (games * 60))], samplesaverages[t+1]['ADC']['championGames'])
    np.put(datasetchampaverages, [int(59 + (games * 60))], samplesaverages[t+1]['ADC']['averageGames'])


    dataset2array(samples[t]['Top'],0,dataset,height,140,games)
    dataset2array(samples[t]['Middle'], 1, dataset, height, 140, games)
    dataset2array(samples[t]['Jungle'], 2, dataset, height, 140, games)
    dataset2array(samples[t]['Support'], 3, dataset, height, 140, games)
    dataset2array(samples[t]['ADC'], 4, dataset, height, 140, games)
    dataset2array(samples[t+1]['Top'], 5, dataset, height, 140, games)
    dataset2array(samples[t+1]['Middle'], 6, dataset, height, 140, games)
    dataset2array(samples[t+1]['Jungle'], 7, dataset, height, 140, games)
    dataset2array(samples[t+1]['Support'], 8, dataset, height, 140, games)
    dataset2array(samples[t+1]['ADC'], 9, dataset, height, 140, games)
    if samples[t]['win'] == 'Win':
        np.put(labels,[int(labelcount)],0)
        labelcount +=1
    else:
        np.put(labels,[int(labelcount)],1)
        labelcount+=1
    games +=1
    t+=2

df_test = pd.DataFrame(samples)
np.savetxt("dataset_array.csv", dataset, delimiter=",")
np.savetxt("dataset_array_champs.csv", datasetchamp, delimiter=",")
np.savetxt("dataset_array_champs_averages.csv", datasetchampaverages, delimiter=",")


np.savetxt("dataset_array_labels.csv",labels, delimiter=",")
print("done")


