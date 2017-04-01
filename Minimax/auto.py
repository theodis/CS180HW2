#!/usr/bin/python2
from shell import *
import sys

board = "-K----NBRRBN--PP----------------pp--nbrrbn----k-"
player = 1
weights1 = sys.argv[1]
weights2 = sys.argv[2]
limit = float(sys.argv[3])

while(True):
    printBoard(board)
    move = ""
    if(player == 1): #Computer 1's turn
        move = getMove(board, player, weights1, limit)
        if(not validateMove(board, player, move)):
            print("Computer " + str(player) + " tried to play an illegal move!")
            break
        print("Computer " + str(player) + " plays move: " + move + " (" + flipMove(move) + ")")
    else: #Computer 2's turn
        move = getMove(board, player, weights2, limit)
        if(not validateMove(board, player, move)):
            print("Computer " + str(player) + " tried to play an illegal move!")
            break
        print("Computer " + str(player) + " plays move: " + move + " (" + flipMove(move) + ")")
    board = playMove(board, player, move)
    player = 2 - player + 1 #Alternate player
    if(isGameOver(board,player) != 0):
        printBoard(board)
        print("Computer " + str(isGameOver(board,player)) + " wins!")
        break;

