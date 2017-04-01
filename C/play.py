#!/usr/bin/python2
from shell import *
import sys

board = "-K----NBRRBN--PP----------------pp--nbrrbn----k-"
player = int(sys.argv[1])
weights = sys.argv[2]
limit = float(sys.argv[3])

while(True):
    printBoard(board)
    move = ""
    if(player == 1): #Human's turn
        while(not validateMove(board, player, move)):
            move = raw_input("> ");
            if(not validateMove(board, player, move)):
                print("Invalid move")
    else: #Computer's turn
        move = getMove(board, player, weights, limit)
        if(not validateMove(board, player, move)):
            print("Computer tried to play an illegal move!")
            break
        print("Computer plays move: " + move)
    board = playMove(board, player, move)
    player = 2 - player + 1 #Alternate player
    if(isGameOver(board,player) != 0):
        printBoard(board)
        print("Player " + str(isGameOver(board,player)) + " wins!")
        break;
