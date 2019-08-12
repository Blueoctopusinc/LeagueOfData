from apiHandlers import ApiHandler
import pandas as pd
import csv
import roleml as roleID
roleDict = {
    "BOTTOM_DUO_SUPPORT": 'Support',
    "BOTTOM_DUO_CARRY": 'Adc',
    "JUNGLE_NONE": 'Jungle',
    "TOP_SOLO": 'Top',
    "MIDDLE_SOLO": 'Middle',
}

euwApiController = ApiHandler("euw1", 'RGAPI-81390dcc-ef16-47d3-a972-1c2aadcf5ec1')

matches = pd.read_csv('/home/joshua/PycharmProjects/dataCollector/0', usecols=[0], names=['match'])
goldData = pd.read_csv('/home/joshua/PycharmProjects/dataCollector/bronzeChampData.csv')
silverData = pd.read_csv('/home/joshua/PycharmProjects/dataCollector/silverChampData.csv')
bronzeData = pd.read_csv('/home/joshua/PycharmProjects/dataCollector/bronzeChampData.csv')
platinumData = pd.read_csv('/home/joshua/PycharmProjects/dataCollector/platinumChampData.csv')
def columnRename(df):
    df.columns = ["assists","banRate","exp","deaths","goldEarned","kills","killingSpree","minionsKilled","enemyJungle","teamJungle",
                  "posNo","posChange","playPercent","damageDealt","damageTaken","totalHeal","wr","champion","role","title"]
print(goldData)
columnRename(goldData)
columnRename(silverData)
columnRename(bronzeData)
columnRename(platinumData)

def featureGenerator(currMatch):
    data = []
    redTeam = {}
    blueTeam = {}

    rankChampData = 0
    matchData = euwApiController.request('match', currMatch)
    matchTimeline = euwApiController.request('timeLine', currMatch)
    if matchData is -1 or None:
        print("API error")
        return -1
    if matchTimeline is -1 or None:
        print("API error")
        return -1
    rank = eloCheck(matchData)
    if rank is None:
        return -1
    print(rank)
    if rank == 'GOLD':
        rankChampData=goldData
    if rank == 'SILVER':
        rankChampData=silverData
    if rank == 'BRONZE':
        rankChampData=bronzeData
    if rank == 'PLATINUM':
        rankChampData=platinumData

    roles=checkRoles(matchData, matchTimeline)
    if roles is None:
        return -1
    matchRoles = roleSwapper(roles)
    for i in matchData['teams']:
        if i['teamId'] == 100:
            blueTeam['win'] = i['win']
        if i['teamId'] == 200:
            redTeam['win'] = i['win']
    for i in matchRoles:
        player = i
        playerRole = matchRoles[i]
        currPlayer = playerFeatures(rankChampData, matchData, player, playerRole)
        if currPlayer == -1:
            print("Invalid participant details, skipping match")
            return -1
        if currPlayer['team'] == 100:
            blueTeam[playerRole]=currPlayer
        if currPlayer['team'] == 200:
            redTeam[playerRole]=currPlayer

    print(blueTeam)
    print(redTeam)
    data.append(redTeam)
    data.append(blueTeam)

    #redchech = json_normalize(redTeam, sep='_')
    #df = pd.DataFrame(data)

    return data
def playerFeatures(champData, match, player, role):
    playerStats = {}
    for i in match['participants']:
        if i['participantId'] == player:
            playerStats['team'] = i['teamId']
            playerStats['champion'] = i['championId']
            playerStats['kills'] = i['stats']['kills']
            playerStats['deaths'] = i['stats']['deaths']
            playerStats['assists'] = i['stats']['assists']
            playerStats['killSpree'] = i['stats']['largestKillingSpree']
            playerStats['damage'] = i['stats']['totalDamageDealt']
            playerStats['gold'] = i['stats']['goldEarned']
            playerStats['cs'] = i['stats']['totalMinionsKilled']
            playerStats['teamJungle'] = i['stats']['neutralMinionsKilledTeamJungle']
            playerStats['enemyJungle'] = i['stats']['neutralMinionsKilledEnemyJungle']
            playerStats['damageTaken'] = i['stats']['totalDamageTaken']
            playerStats['totalHeal'] = i['stats']['totalHeal']
    for i in match['participantIdentities']:
        if i['participantId']==player:
            accID = i['player']['accountId']
            games,winrate=playerWinrate(accID, playerStats['champion'])
            if games == -1:
                print('games Calculation Error')
                return -1
            if winrate == -1:
                print('winrate calc error')
                return -1
            else:
                playerStats['playerWinrateLast25'] = winrate
                playerStats['championGames'] = games
    return playerStats

def playerWinrate(accountID, championID):
    wins = 0
    loss = 0
    champMatches=euwApiController.champrequest('champMatchList', accountID, championID)
    if champMatches ==-1:
        return -1, -1
    x=0
    totalGames = len(champMatches['matches'])
    if totalGames < 25:
        searchCrit = totalGames
    else:
        searchCrit = 25

    while x < searchCrit:
        i=champMatches['matches'][x]
        currMatch = i['gameId']
        match = euwApiController.request('match', currMatch)
        if match == None:
            return None, None
        if match == -1:
            return None, None
        for i in match['participantIdentities']:
            if i['player']['accountId'] == accountID:
                currParId = i['participantId']
                for i in match['participants']:
                    if i['participantId']==currParId:
                        if i['stats']['win'] == True:
                            wins+=1
                            x+=1
                        else:
                            loss+=1
                            x+=1
    winPercent = wins/searchCrit
    return totalGames, winPercent



def checkRoles(matchData, matchTimeline):
    try:
        check = roleID.predict(matchData, matchTimeline)
    except:
        print('warning')
        return None
    else:
        return check

def eloCheck(match):
    toCheck = match['participantIdentities'][0]['player']['summonerId']
    leagueStat = euwApiController.request('league', toCheck)
    print(leagueStat)
    if leagueStat is -1 or None:
        return None
    for i in leagueStat:
        print(i)
        if i['queueType'] == 'RANKED_SOLO_5x5':
            return i['tier']

def roleSwapper(roles):
    newRoles = {}
    print(roles)
    i=1
    while i <= len(roles):
        roleChange = roles[i]
        newRoles[i] = roleDict[roleChange]
        print(newRoles)
        i+=1
    return newRoles

print(len(matches))

processed_matches = []
dataset = []
limit = 200
count = 0

for i in matches['match']:
    if count < limit:
        match = featureGenerator(i)
        if match != -1:
            dataset.extend(match)
            processed_matches.append(match)
            count +=1
df_processed_matches = pd.DataFrame(dataset)
df_dataset = pd.DataFrame(dataset)
df_dataset.to_csv("dataset_0")
df_processed_matches.to_csv("processed_matches_0")
