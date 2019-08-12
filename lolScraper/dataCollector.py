from apiHandlers import ApiHandler
import pandas as pd
import csv

import time
region = 'euw1'
#Const Variables
riotApiKeys = ['RGAPI-d21cc2f8-d166-4a8e-85d0-2905ef93d4c2']

#roles = get_roles(champion_roles,[32, 103, 22, 12, 266])

#print({role.name: champion.name for role, champion in roles[0].items()})
def pullMatch(seed, batch, lim, apiController, fileName):

    #    print(redTeam)

    #Takes a matchlist (in the form of a dictionary/parsed json) and finds unique match ID's and appends it to the match
    #ID list
    def matchChecker(matchList):
        if matchList == -1:
            return
        i = 0
        for i in matchList['matches']:
            currMatch = i['gameId']
            if currMatch not in matchIdList:
                    matchIdList.append(currMatch)
                   # print("match added")

        return
    #With a match id, pulls down a match from the riot match endpoint the api controller, iterates through the
    #the participants and stores any unique id's, then requests a match list for the unique ID and sends it to the
    #Match checker function
    def findUsers(matchID):
        if matchID is None:
            return None
        currMatch = myApiController.request('match', matchID)
        x = 0
        if currMatch is -1:
            return
        if currMatch is None:
            return
        else:
            while x < len(currMatch['participantIdentities']):
                temp = currMatch['participantIdentities'][x]['player']['accountId']
                if temp not in idList:
                    idList.append(temp)
                    checkUser = myApiController.request('matchList', temp)
                    if checkUser is not None:
                        matchChecker(checkUser)
                    return currMatch
                x += 1


    myApiController = apiController

    batchInterval = batch
    idList = []
    idList.append('9pOjRCioBH6vVb4oLey-ijMuXEciOL3DomwqsB8O1QqOtMM')
    matchIdList = []
    matches = []
    matchChecker(seed)
    i = 0
    while len(matchIdList) < lim:
        if len(matches) < batch:
            print(matchIdList[i])
            thisMatch = findUsers(matchIdList[i])
            if thisMatch is not None:
                print("is this edit showing up?")
#if thisMatch is not None:
#matchFeatureMaker(thisMatch)
        print(len(matchIdList), " Matches" )
        i+=1

    df = pd.DataFrame(matchIdList)
    ts = time.time()
    df.to_csv("matches", index=False)

def fileWriter(input, path):
    with open(path,'a') as newFile:
        writer = csv.DictWriter(newFile, input.keys())
        writer.writerow(input)

euwApiController = ApiHandler("euw1", riotApiKeys[0])
na1ApiController = ApiHandler("na1", riotApiKeys[0])
naA2piController = ApiHandler('na1', riotApiKeys[1])
euw2ApiController = ApiHandler('euw1', riotApiKeys[1])


seed = euwApiController.request('matchList', '9pOjRCioBH6vVb4oLey-ijMuXEciOL3DomwqsB8O1QqOtMM')
pullMatch(seed, 200000, 200000, euwApiController, 'EUW')


