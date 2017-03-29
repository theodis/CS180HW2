class Game():
    def __init__(self):
        self.callback = []
        return
    def copyGame(self):
        pass
    def generateMoves(self):
        return []
    def boardState(self):
        return []
    def playMove(self, move):
        for f in self.callback:
            f(self, move)
        return
    def addMoveCallback(self, cb):
        self.callback.append(cb)
    def eval(self):
        return 0
    def isGameOver(self):
        return 0
    def curentPlayer(self):
        return 1

    @property
    def width(self):
        return 0
    @property
    def height(self):
        return 0
