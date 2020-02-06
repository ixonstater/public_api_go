import json
from resources import const
from datetime import datetime
from threading import Thread
from time import sleep
import mysql.connector
from resources import credentials
from resources import config

class Matches:

    def __init__(self):
        self.matchDump = {}
        self.databaseQueue = []
        self.sleepCount = 0

        self.bgProcess = Thread(target=self.backgroundProcessing)
        self.bgProcess.daemon = True
        self.bgProcess.start()

    def setMatchState(self, accessToken, newState):
        self.matchDump[accessToken].gameState = newState

    def getMatchState(self, accessToken):
        return {
            'state': self.matchDump[accessToken].gameState,
            'previousMove': self.matchDump[accessToken].previousTurn
        }

    def newStateExists(self, accessToken, whosTurn):
        return self.matchDump[accessToken].gameState['whosTurn'] != whosTurn

    def addMatch(self, accessToken, newMatch):
        self.matchDump[accessToken] = newMatch

    def tokenExists(self, token):
        return token in self.matchDump

    def addToDBQueue(self, accessToken, nextMove):
        self.databaseQueue.append(
            {
                'accessToken': accessToken,
                'nextMove': nextMove,
                'state': self.matchDump[accessToken].gameState,
                'previousTurn': self.matchDump[accessToken].previousTurn
            }
        )

    def checkWhosTurn(self, accessToken, whosTurn):
        matchData = self.matchDump[accessToken]
        return matchData.gameState['whosTurn'] == whosTurn

    def setPreviousTurn(self, accessToken, move):
        self.matchDump[accessToken].previousTurn = move

    def getColor(self, accessToken, userToken):
        match = self.matchDump[accessToken]
        if(match.gameState['whosTurn'] == const.BLACK):
            return const.BLACK

        elif (match.gameState['whosTurn'] == const.WHITE):
            return const.WHITE

        else:
            return const.EMPTY
    
    def indexIsEmpty(self, accessToken, index):
        return self.matchDump[accessToken].gameState['boardState'][index[0]][index[1]] == const.EMPTY

    def setLastUpdated(self, accessToken):
        self.matchDump[accessToken].lastUpdated = datetime.now()

    def backgroundProcessing(self):
        while(True):
            if(self.sleepCount >= const.RESET_COUNT):
                self.sleepCount = 0

            self.moveStatesToDB()
            self.removeInactiveMatches()
            
            self.sleepCount += 1
            sleep(const.BG_SLEEP_INTERVAL)

    def removeInactiveMatches(self):
        if (self.sleepCount % const.REMOVE_MATCHES_COUNT == 0 and config.REMOVE_INACTIVE_MATCHES):
            now = datetime.now()
            keys = list(self.matchDump.keys())

            for key in keys:
                diff = now - self.matchDump[key].lastUpdated
                if(diff.seconds >= const.DELETE_MATCH_TIMEOUT):
                    del self.matchDump[key]

    def moveStatesToDB(self):
        if (self.sleepCount % const.MOVE_TO_DB_COUNT == 0 and config.LOG_TO_DATABASE):
            connection = mysql.connector.connect(
                host = 'localhost',
                user = credentials.username,
                passwd = credentials.password,
                database = 'go'
            )
            cursor = connection.cursor()

            for state in self.databaseQueue:
                
                accessToken = state['accessToken']
                previousTurn = json.dumps(state['previousTurn'])
                nextMove = json.dumps(state['nextMove'])
                state = json.dumps(state['state'])

                query = F'insert into gamestates (accesstoken, nextmove, previousmove, state) values (\'{accessToken}\', \'{nextMove}\', \'{previousTurn}\', \'{state}\')'
                cursor.execute(query)

            connection.commit()
            self.databaseQueue = []


class Match:

    def __init__(self):
        self.lastUpdated = datetime.now()
        self.previousTurn = None
        self.gameState = {
            "whosTurn": const.BLACK,
            "boardState": [
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            ]
        }


class Model:
    def __init__():
        pass