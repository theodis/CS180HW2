#!/usr/bin/python2
import random
from shell import *
import tempfile
import os
import copy
from subprocess import *

class Sequence:
    def __init__(self):
        self.map = {}
        self.generation = 0
        self.random = 1
        
    def seedRandom(self):
        pieces = ['K','N','B','R','P']

        #Set the space values
        printMap = {}
        printMap['-'] = []
        for j in range(8):
            printMap['-'].append([])
            for i in range(6):
                printMap['-'][j].append(random.randint(1,65534))

        #Set the black piece values
        for piece in pieces:
            printMap[piece] = []
            for j in range(8):
                printMap[piece].append([])
                for i in range(6):
                    printMap[piece][j].append(random.randint(0,printMap['-'][j][i] - 1))
                
        #Set the white piece values
        for piece in pieces:
            printMap[piece.lower()] = []
            for j in range(8):
                printMap[piece.lower()].append([])
                for i in range(6):
                    printMap[piece.lower()][j].append(random.randint(printMap['-'][j][i] + 1, 65535))

        self.generation = 0
        self.map = printMap
        self.random = 1

    def seedString(self, string):
        pieceOrder = ['-','K','N','B','R','P','k','n','b','r','p']
        self.generation = int(string[0:8], 16)
        ind = 8;
        self.map = {}
        for piece in pieceOrder:
            self.map[piece] = []
            for j in range(8):
                self.map[piece].append([])
                for i in range(6):
                    self.map[piece][j].append(int(string[ind:ind+4], 16))
                    ind += 4
        self.random = self.generation == 0
    def seedFile(self, filename):
        with open(filename, 'r') as fp:
            self.seedString(fp.read())
    def splice(self, other):
        ret = Sequence()
        ret.seedRandom() #Random data not really needed just building structure
        for piece in self.map.keys():
            for j in range(8):
                for i in range(6):
                    t = random.random()
                    interpolated = int(round((self.map[piece][j][i] * t) + (other.map[piece][j][i] * (1 - t))))
                    if(random.randint(0,200) == 0): #mutation
                        if(random.randint(0,1) == 0): #multiply
                            interpolated *= random.randint(2,5)
                            if(interpolated > 65535):
                                interpolated = 65535
                        else: #divide
                            interpolated /= random.randint(2,5)
                        interpolated = int(interpolated)

                    ret.map[piece][j][i] = interpolated
        ret.random = False
        ret.generation = max(self.generation, other.generation) + 1
        return ret
    def __str__(self):
        pieceOrder = ['-','K','N','B','R','P','k','n','b','r','p']
        output = ("%08x" % self.generation).upper()
        for piece in pieceOrder:
            for j in range(8):
                for i in range(6):
                    output += ("%04x" % self.map[piece][j][i]).upper()
        return output

def sequenceFile(seq):
    fp = tempfile.NamedTemporaryFile(delete=False)
    fp.write(str(seq))
    fp.close()
    return fp.name

def getLastBest():
    stdout_data = check_output(['tail','-1','best.txt'])
    if(stdout_data == ""):
        return None
    ret = Sequence()
    ret.seedString(stdout_data)
    return ret

def compete(a, b, randomSwap = True, limit = 1, show = False):
    if(randomSwap and random.randint(0,1) == 0): #swap
        temp = a
        a = b
        b = temp
    af = sequenceFile(a)
    bf = sequenceFile(b)
    player = 1
    board = "-K----NBRRBN--PP----------------pp--nbrrbn----k-"
    ret = None
    while(True):
        if(show):
            printBoard(board)
        move = ""
        if(player == 1): #Computer 1's turn
            move = getMove(board, player, af, limit)
            if(not validateMove(board, player, move)):
                print("Computer " + str(player) + " tried to play an illegal move! " + move)
                break;
        else: #Computer 2's turn
            move = getMove(board, player, bf, limit)
            if(not validateMove(board, player, move)):
                print("Computer " + str(player) + " tried to play an illegal move! " + move)
                break
        if(show):
            print("Computer " + str(player) + " plays move: " + move + " (" + flipMove(move) + ")")
        board = playMove(board, player, move)
        player = 2 - player + 1 #Alternate player
        if(isGameOver(board,player) != 0):
            if(show):
                printBoard(board)
            if(isGameOver(board,player) == 1):
                ret = a
            else:
                ret = b
            break;
    os.remove(af)
    os.remove(bf)
    return ret

def bracketCompete(seqList):
    results = [copy.copy(seqList)]

    while(True):
        cur = results[-1]
        if(len(cur) <= 1):
            break
        results.append([])
        for i in range(len(cur)/2):
            a = cur[i*2]
            b = cur[i*2+1]
            winner = compete(a,b)
            results[-1].append(winner)
    ret = []
    for i in range(len(results), 1 , -1):
        for s in results[i-1]:
            if not s in ret:
                ret.append(s)
    return ret

roundCount = 1
count = 32
league = []

with open("genes.txt", "r") as fp:
    for line in fp.readlines():
        seq = Sequence()
        seq.seedString(line)
        league.append(seq)
while(len(league) < count):
    seq = Sequence()
    seq.seedRandom()
    league.append(seq)

while(True):
    ordered = bracketCompete(league)
    randoms = (count - len(ordered)) / 2
    league = ordered

    #populate new randoms
    for i in range(randoms):
        seq = Sequence()
        seq.seedRandom()
        league.append(seq)
    #add splices

    i = 0
    while(len(league) < count):
        seq = league[i].splice(league[i+1])
        league.append(seq)
        i += 2

    #Is there a new best?
    twinner = league[i]
    oldbest = getLastBest()
    if(oldbest != None and str(twinner) != str(oldbest)):
        winner = compete(twinner,oldbest)
        if(winner == twinner):
            with open("best.txt", "a") as fp:
                fp.write(str(winner) + "\n")
    elif(oldbest == None):
        with open("best.txt", "a") as fp:
            fp.write(str(twinner) + "\n")

    #write out new pool
    with open("genes.txt", "w") as fp:
        for seq in league:
            fp.write(str(seq) + "\n")
    print("Round " + str(roundCount) + " finished")
    roundCount += 1
