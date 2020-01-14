from pyramid.response import Response
from resources import const

class SubmitTurn:

    def __init__(self, context, request):
        self.request = request
        self.context = context
        self.validRequest = True
        self.response = None

    def processRequest(self):
        self.sanitizeRequest()

        if(self.validRequest):
            self.validateWhosTurn()

        if(self.validRequest):
            self.context.matches.addToDBQueue(self.requestBody['accessToken'], [self.requestBody['x'], self.requestBody['y']])
            self.updateGameState()

        return self.response

    def sanitizeRequest(self):
        self.requestBody = self.request.json
        if(
            not (
            'x' in self.requestBody and
            'y' in self.requestBody and
            'accessToken' in self.requestBody and
            'userToken' in self.requestBody
            )
        ):
            self.validRequest = False
            self.response = Response('An internal error occured.')

        elif(self.requestBody['x'] >= 19 or self.requestBody['y'] >= 19):
            self.validRequest = False
            self.response = Response('An internal error occured.')

        elif(not self.context.matches.tokenExists(self.requestBody['accessToken'])):
            self.validRequest = False
            self.response = Response('An internal error occured.')

    def validateWhosTurn(self):
        if(self.context.matches.checkWhosTurn(self.requestBody['accessToken'], self.requestBody['userToken'])):
            self.validRequest = False
            self.response = Response('Not your turn.')

    def updateGameState(self):
        nextMove = [self.requestBody['x'], self.requestBody['y']]
        matchData = self.context.matches.getMatchState(self.requestBody['accessToken'])
        color = self.context.matches.getColor(self.requestBody['accessToken'], self.requestBody['userToken'])
        deadStoneFinder = FindDeadStones(matchData['boardState'], nextMove, color)
        stonesToRemove = deadStoneFinder.findStonesToRemove()
        newBoard = self.removeStones(stonesToRemove, matchData['boardState'])
        newBoard[nextMove[0]][nextMove[1]] = color
        newState = {
            'boardState': newBoard,
            'whosTurn': const.BLACK if color == const.WHITE else const.WHITE
        }
        self.context.matches.setMatchState(self.requestBody['accessToken'], newState)
        self.response = Response(self.requestBody['accessToken'])

    def removeStones(self, stonesToRemove, board):
        for stone in stonesToRemove:
            board[stone[0]][stone[1]] = const.EMPTY
        return board
            

    
class FindDeadStones:

    def __init__(self, board, nextMove, color):
        self.visitedSet = set()
        self.toCheckQueue = []
        self.board = board
        self.nextMove = nextMove
        self.friendlyColor = color
        self.toRemove = []
        self.friendCode = 0
        self.emptyCode = 1
        self.enemyCode = 2

    def findStonesToRemove(self):
        for x in range(0, 19):
            for y in range(0, 19):
                if(self.board[x][y] != 0):
                    stoneGroup, lifeCount = self.findStonesToRemoveHelper(x,y)
                    if(lifeCount == 0):
                        self.toRemove.append(stoneGroup)

        return self.toRemove

    def findStonesToRemoveHelper(self,x,y):
        lifeCount = 0
        stoneGroup = []
        stoneLocation = [x,y]
        self.toCheckQueue.append(stoneLocation)

        while(self.toCheckQueue):
            currentStoneLocation = self.toCheckQueue.pop()
            stoneGroup.append(currentStoneLocation)
            stoneName = x + ',' + y
            self.visitedSet.add(stoneName)

            surroundings = self.getStoneFriendsAndLives(currentStoneLocation)
            for index in surroundings:
                if(index[1] == self.emptyCode):
                    lifeCount += 1
                
                elif(index[1] == self.friendCode):
                    self.toCheckQueue.append(index[0])



        return [stoneGroup, lifeCount]

    def getStoneFriendsAndLives(self, location):
        x = location[0]
        y = location[1]

        if(x == 0):
            if(y == 0):
                locations = [None, [1,0], [0,1], None]
                return [[],]

            elif(y == 18):
                locations = [[17, 0], [18,1], None, None]

            else:
                locations = [[0, y-1], [1, y], [0, y+1], None]

        elif(x == 18):
            if(y == 0):
                locations = [None, None, [18, 1], [17, 0]]

            elif(y == 18):
                locations = [[18, 17], None, None, [17, 18]]

            else:
                locations = [[18, y-1], None, [18, y+1], [17, y]]

        elif(y == 0):
            locations = [None, [0, x+1], [1, x], [0, x-1]]

        elif(y == 18):
            locations = [[17, x], [18, x+1], None, [18, x-1]]

        else:
            locations = [[x, y-1], [x+1, y], [x, y+1], [x-1, y]]

        return zip(locations, map(self.blankFriendEnemy, locations))

    def blankFriendEnemy(self, location):
        if(self.board[location[0]][location[1]] == const.EMPTY):
            return self.emptyCode

        elif (self.board[location[0]][location[1]] == self.friendlyColor):
            return self.friendCode

        else:
            return self.enemyCode