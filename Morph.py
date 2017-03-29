from Game import Game
from MorphEval import morphEval
from Minimax import miniMax
import copy

class Morph(Game):
    def __init__(self):
        super().__init__()
        self.board = [
            ['-','K','-','-','-','-'],
            ['N','B','R','R','B','N'],
            ['-','-','P','P','-','-'],
            ['-','-','-','-','-','-'],
            ['-','-','-','-','-','-'],
            ['-','-','p','p','-','-'],
            ['n','b','r','r','b','n'],
            ['-','-','-','-','k','-']
        ]
        self.curplayer = 1
        self.wking = True
        self.bking = True
        self.gameover = 0

    def currentPlayer(self):
        return self.curplayer

    def copyGame(self):
        ret = Morph(self)
        ret.board = self.boardState()
        ret.curplayer = self.curplayer
        ret.wking = self.wking
        ret.bking = self.bking
        ret.gameover = self.gameover
        return ret

    def isonboard(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def player(self, x, y):
        if(not self.isonboard(x,y) or self.board[y][x] == '-'):
            return 0
        if(self.board[y][x].islower()):
            return 1
        if(self.board[y][x].isupper()):
            return 2
        return 0

    def canattack(self, sx, sy, ex, ey):
        sp = self.player(sx,sy)
        ep = self.player(ex,ey)
        return sp != 0 and ep != 0 and sp != ep

    def attack(self, sx, sy, ex, ey):
        if(self.canattack(sx,sy,ex,ey)):
            return [[sx, sy, ex, ey]]
        return []

    def canmove(self, sx, sy, ex, ey):
        sp = self.player(sx,sy)
        ep = self.player(ex,ey)
        return sp != 0 and ep == 0 and self.isonboard(ex,ey)

    def move(self, sx, sy, ex, ey):
        if(self.canmove(sx,sy,ex,ey)):
            return [[sx, sy, ex, ey]]
        return []

    def canmoveorattack(self, sx, sy, ex, ey):
        sp = self.player(sx,sy)
        ep = self.player(ex,ey)
        return sp != 0 and sp != ep and self.isonboard(ex,ey)

    def moveorattack(self, sx, sy, ex, ey):
        if(self.canmoveorattack(sx,sy,ex,ey)):
            return [[sx, sy, ex, ey]]
        return []

    def trace(self, sx, sy, dx, dy, move, attack):
        ret = []
        sp = self.player(sx,sy)
        cx = sx + dx
        cy = sy + dy
        while self.isonboard(cx,cy):
            cp = self.player(cx,cy)
            if(sp == cp):
                break
            elif(move and self.canmove(sx,sy,cx,cy)):
                ret.append([sx,sy,cx,cy])
            elif(attack and self.canattack(sx,sy,cx,cy)):
                ret.append([sx,sy,cx,cy])
                break
            cx += dx
            cy += dy

        return ret

    def isGameOver(self):
        if(not self.bking):
            return 1
        if(not self.wking):
            return 2
        if(len(self.generateMoves()) == 0):
            return 2 - self.curplayer + 1
        return 0

    def generateMoves(self):
        if(self.gameover != 0):
            return []
        ret = []
        bw = self.width
        bh = self.height

        for y in range(0, bh):
            for x in range(0, bw):
                piece = self.board[y][x]
                if(self.player(x,y) != self.curplayer):
                    continue
                elif(piece == 'p'):
                    #Player 1 pawn
                    #Moves up or attacks diagonally up
                    ret.extend(self.move(x,y,x,y-1))
                    ret.extend(self.attack(x,y,x-1,y-1))
                    ret.extend(self.attack(x,y,x+1,y-1))
                elif(piece == 'P'):
                    #Player 2 pawn
                    #Moves down or attacks diagonally down
                    ret.extend(self.move(x,y,x,y+1))
                    ret.extend(self.attack(x,y,x-1,y+1))
                    ret.extend(self.attack(x,y,x+1,y+1))
                elif(piece == 'k'):
                    #Player 1 king
                    #Move or capture to the left
                    #Capture to the right
                    ret.extend(self.moveorattack(x,y,x-1,y))
                    ret.extend(self.attack(x,y,x+1,y))
                elif(piece == 'K'):
                    #Player 2 king
                    #Move or capture to the right
                    #Capture to the left
                    ret.extend(self.moveorattack(x,y,x+1,y))
                    ret.extend(self.attack(x,y,x-1,y))
                elif(piece == 'n'):
                    #Player 1 knight
                    #Knights move in L shaped paths, 1 space in one axis
                    #and 2 in the other
                    #Can hop over units
                    #Move or capture up
                    #Capture only down
                    ret.extend(self.moveorattack(x,y,x-1,y-2))
                    ret.extend(self.attack(x,y,x-1,y+2))
                    ret.extend(self.moveorattack(x,y,x+1,y-2))
                    ret.extend(self.attack(x,y,x+1,y+2))
                    ret.extend(self.moveorattack(x,y,x-2,y-1))
                    ret.extend(self.attack(x,y,x-2,y+1))
                    ret.extend(self.moveorattack(x,y,x+2,y-1))
                    ret.extend(self.attack(x,y,x+2,y+1))
                elif(piece == 'N'):
                    #Player 2 knight
                    #Knights move in L shaped paths, 1 space in one axis
                    #and 2 in the other
                    #Can hop over units
                    #Move or capture down
                    #Capture only up
                    ret.extend(self.attack(x,y,x-1,y-2))
                    ret.extend(self.moveorattack(x,y,x-1,y+2))
                    ret.extend(self.attack(x,y,x+1,y-2))
                    ret.extend(self.moveorattack(x,y,x+1,y+2))
                    ret.extend(self.attack(x,y,x-2,y-1))
                    ret.extend(self.moveorattack(x,y,x-2,y+1))
                    ret.extend(self.attack(x,y,x+2,y-1))
                    ret.extend(self.moveorattack(x,y,x+2,y+1))
                elif(piece == 'b'):
                    #Player 1 bishop
                    #Move or capture up diagonally
                    #Capture only down diagonally
                    ret.extend(self.trace(x,y,-1,-1,True,True))
                    ret.extend(self.trace(x,y,1,-1,True,True))
                    ret.extend(self.trace(x,y,-1,1,False,True))
                    ret.extend(self.trace(x,y,1,1,False,True))
                elif(piece == 'B'):
                    #Player 2 bishop
                    #Move or capture down diagonally
                    #Capture only up diagonally
                    ret.extend(self.trace(x,y,-1,1,True,True))
                    ret.extend(self.trace(x,y,1,1,True,True))
                    ret.extend(self.trace(x,y,-1,-1,False,True))
                    ret.extend(self.trace(x,y,1,-1,False,True))
                elif(piece == 'r'):
                    #Player 1 rook
                    #Move or capture straight up or sidways
                    #Capture only straight down
                    ret.extend(self.trace(x,y,0,-1,True,True))
                    ret.extend(self.trace(x,y,-1,0,True,True))
                    ret.extend(self.trace(x,y,1,0,True,True))
                    ret.extend(self.trace(x,y,0,1,False,True))
                elif(piece == 'R'):
                    #Player 2 rook
                    #Move or capture straight down or sidways
                    #Capture only straight up
                    ret.extend(self.trace(x,y,0,1,True,True))
                    ret.extend(self.trace(x,y,-1,0,True,True))
                    ret.extend(self.trace(x,y,1,0,True,True))
                    ret.extend(self.trace(x,y,0,-1,False,True))

        return ret
    def boardState(self):
        return copy.deepcopy(self.board)
    def playMove(self, move):
        sx = move[0]
        sy = move[1]
        ex = move[2]
        ey = move[3]
        sp = self.board[sy][sx]
        rp = self.board[ey][ex]
        if(sp == 'b'):
            ep = 'n'
        elif(sp == 'B'):
            ep = 'N'
        elif(sp == 'r'):
            ep = 'b'
        elif(sp == 'R'):
            ep = 'B'
        elif(sp == 'n'):
            ep = 'r'
        elif(sp == 'N'):
            ep = 'R'
        else:
            ep = sp
        self.board[sy][sx] = '-'
        self.board[ey][ex] = ep

        self.curplayer = 2 - self.curplayer + 1

        if(rp == 'k'):
            self.wking = False
        if(rp == 'K'):
            self.bking = False

        self.gameover = self.isGameOver()
        super().playMove(move)

    @property
    def width(self):
        return len(self.board[0])
    @property
    def height(self):
        return len(self.board)
