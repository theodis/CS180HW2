#!/usr/bin/python

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

output = "00000000"
for piece in pieceOrder:
    for j in range(8):
        for i in range(6):
            output += ("%04x" % pieceMap[piece]).upper()
print(output)
