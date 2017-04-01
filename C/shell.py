#!/usr/bin/python2
from subprocess import *

def printBoard(board):
    p = Popen(['./printboard'], stdout=PIPE, stdin=PIPE)
    stdout_data = p.communicate(input=board)[0]
    print(stdout_data)

def getMove(board, player, weights, limit):
    p = Popen(['./getmove',str(player),weights,str(limit)], stdout=PIPE, stdin=PIPE)
    stdout_data = p.communicate(input=board)[0]
    return stdout_data

def isGameOver(board, player):
    p = Popen(['./isgameover',str(player)], stdout=PIPE, stdin=PIPE)
    stdout_data = p.communicate(input=board)[0]
    return int(stdout_data)

def playMove(board, player, move):
    p = Popen(['./playmove',str(player), move], stdout=PIPE, stdin=PIPE)
    stdout_data = p.communicate(input=board)[0]
    return stdout_data

def validateMove(board, player, move):
    if(len(move) < 4):
        return False
    p = Popen(['./validatemove',str(player), move], stdout=PIPE, stdin=PIPE)
    stdout_data = p.communicate(input=board)[0]
    return stdout_data == "1"
