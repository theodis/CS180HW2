from Game import Game

def miniMax(board, evalFunc, maxdepth):
    bestMove = None
    bestScore = -1000000
    moves = board.generateMoves()
    for move in moves:
        boardCopy = board.copyGame()
        boardCopy.playMove(move)
        score = minFunc(boardCopy, evalFunc, maxdepth)
        if(score > bestScore):
            bestScore = score
            bestMove = move
    return bestMove

def maxFunc(board, evalFunc, depthleft):
    go = board.isGameOver()
    cp = board.currentPlayer()
    bestScore = -1000000
    bestMove = None
    if(go != 0 and go == cp):
        return 1000000
    elif(go != 0 and go != cp):
        return -1000000
    elif(depth <= 0):
        return evalFunc(board)

    moves = board.generateMoves()
    for move in moves:
        boardCopy = board.copyGame()
        boardCopy.playMove(move)
        score = minFunc(board, evalFunc, depthleft - 1)
        if(score > bestScore):
            bestScore = score
    return bestScore


def minFunc(board, evalFunc, depthleft):
    go = board.isGameOver()
    cp = board.currentPlayer()
    bestScore = 1000000
    bestMove = None
    if(go != 0 and go == cp):
        return 1000000
    elif(go != 0 and go != cp):
        return -1000000
    elif(depth <= 0):
        return evalFunc(board)

    moves = board.generateMoves()
    for move in moves:
        boardCopy = board.copyGame()
        boardCopy.playMove(move)
        score = maxFunc(board, evalFunc, depthleft - 1)
        if(score < bestScore):
            bestScore = score
    return bestScore
