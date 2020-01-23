import json
from resources import const
from datetime import datetime
from threading import Thread
from time import sleep

class Matches:

    def __init__(self):
        self.matchDump = {}
        self.databaseQueue = []
        self.bgRemoveInactiveMatches = Thread(target=self.removeInactiveMatches)
        self.bgRemoveInactiveMatches.daemon = True
        self.bgRemoveInactiveMatches.start()

    def setMatchState(self, accessToken, newState):
        self.matchDump[accessToken].gameState = newState

    def getMatchState(self, accessToken):
        return self.matchDump[accessToken].gameState

    def newStateExists(self, accessToken, whosTurn):
        return self.matchDump[accessToken].gameState['whosTurn'] != whosTurn

    def addMatch(self, accessToken, newMatch):
        self.matchDump[accessToken] = newMatch

    def tokenExists(self, token):
        return token in self.matchDump

    def addToDBQueue(self, accessToken, nextMove):
        pass

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

    def removeInactiveMatches(self):
        while(True):
            now = datetime.now()
            keys = list(self.matchDump.keys())

            for key in keys:
                diff = now - self.matchDump[key].lastUpdated
                if(diff.seconds >= const.INACTIVE_TIMEOUT):
                    del self.matchDump[key]

            sleep(const.MATCH_REMOVAL_INTERVAL)

    def moveStatesToDB(self):
        pass


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