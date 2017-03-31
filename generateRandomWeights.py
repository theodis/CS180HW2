#!/usr/bin/python
import random

pieceMap = {
    '-' : 8,
    'K' : 0,
    'N' : 2,
    'B' : 2,
    'R' : 2,
    'P' : 6, 
    'k' : 16,
    'n' : 14,
    'b' : 14,
    'r' : 14,
    'p' : 10
}

pieceOrder = ['-','K','N','B','R','P','k','n','b','r','p']
pieces = ['K','N','B','R','P']

printMap = { }

#Set the space values
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


output = "00000000"
for piece in pieceOrder:
    for j in range(8):
        for i in range(6):
            output += ("%04x" % printMap[piece][j][i]).upper()
print(output)
