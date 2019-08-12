import requests
import time
#Class to handle endpoints, chose to create my own api handler so multiple could be instantiated to make requests
#from multiple endpoints in matchprocessor
class ApiHandler():

    endPoints = {
    "match": 'match/v4/matches/',
    "matchList": 'match/v4/matchlists/by-account/',
    "timeLine": 'match/v4/timelines/by-match/',
    "league": 'league/v4/positions/by-summoner/',
    "champMatchList": 'match/v4/matchlists/by-account/'

}
    #constants
    apiCalls = 0

    def __init__(self, selRegion, apiKey):
        self.clock = time.clock()
        self.region = 'https://' + selRegion + '.api.riotgames.com/lol/'
        self.apiKey = apiKey

    def limitCheck():
        if self.clock <= 2 and self.apiCalls >= 20 or self.clock <= 120 and self.apiCalls >= 200:
            return True
        else:
            return False


    def request(self, endPoint, id, param1=""):
        check = limitCheck
        if check:
            time.sleep(30)
            print("API limit reached, sleeping")
        else:
            self.apiCalls+=1
            #print(self.apiCalls, 'API Calls')
            queue = "?"
            if endPoint == 'champMatchList':
                queue == '?champion={champ}&queue=420&endindex=100&'.format(champ=param1)
            if endPoint == 'matchList':
                queue = "?queue=420&endindex=100&"
            apiKey = "api_key=" + self.apiKey
            if self.apiCalls == 324:
                print('check')
            r = requests.get(self.region + self.endPoints.get(endPoint) + str(id) + queue +  apiKey)
            myJson = r.json()
            # print(myJson)
            if r.status_code == 404:
                return None
            if r.status_code == 429:
                print("Oh no, exceeded request limit sleeping for 30s")
                time.sleep(30)
                self.request(endPoint, id, param1)
            if r.status_code != 200:
                print("invalid request", r.status_code)
                return -1
            return r.json()

    def champrequest(self, endPoint, id, param1):
        check = limitCheck
        if check:
            time.sleep(30)
            print("API limit reached, sleeping")
        else:
            self.apiCalls+=1
            #print(self.apiCalls, 'API Calls')
            queue = "?champion="
            queue2 = "&queue=420&endindex=50&"
            apiKey = "api_key=" + self.apiKey
            #print(self.region + self.endPoints.get(endPoint) + str(id) + queue + str(param1) + queue2 +  apiKey)
            if self.apiCalls == 324:
                print(endPoint, id, param1)
            r = requests.get(self.region + self.endPoints.get(endPoint) + str(id) + queue + str(param1) + queue2 +  apiKey)

            myJson = r.json()
            # print(myJson)
            if r.status_code == 404:
                return -1
            if r.status_code == 429:
                print("Oh no, exceeded request limit sleeping for 30s")
                time.sleep(30)
                self.champrequest(endPoint, id, param1)
            if r.status_code != 200:
                print("invalid request", r.status_code)
                return -1
            return r.json()



