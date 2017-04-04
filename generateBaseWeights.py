#!/usr/bin/python

pieceMap = {
    '-' : 32767,
    'K' : 0,
    'N' : 16384,
    'B' : 16384,
    'R' : 16384,
    'P' : 24576,
    'k' : 65535,
    'n' : 49151,
    'b' : 49151,
    'r' : 49151,
    'p' : 40959
}

pieceOrder = ['-','K','N','B','R','P','k','n','b','r','p']

output = "00000000"
for piece in pieceOrder:
    for j in range(8):
        for i in range(6):
            output += ("%04x" % pieceMap[piece]).upper()
print(output)
