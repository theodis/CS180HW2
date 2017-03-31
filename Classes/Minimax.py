from Classes.Game import Game
import time

def miniMax(board, evalFunc, timelimit):
    global limit
    limit = time.clock() + timelimit
    globalBestMove = None
    bestMove = None
    bestScore = -1000001
    moves = board.generateMoves()
    maxdepth = 1
    while True:
        if(globalBestMove != None):
            moves.remove(globalBestMove)
            moves.insert(0,globalBestMove)
        for move in moves:
            board.playMove(move)
            score = miniMaxFunc(board, evalFunc, maxdepth, False, -1000000, 1000000)
            board.undoMove()
            if(time.clock() > limit):
                break
            if(score > bestScore):
                bestScore = score
                bestMove = move
        if(time.clock() <= limit):
            print(str(limit - time.clock()) + " " + str(bestScore) + " " + str(maxdepth))
            print(bestMove)
            globalBestMove = bestMove
            maxdepth += 1
        else:
            break
    return globalBestMove

def miniMaxFunc(board, evalFunc, depthleft, ismax, alpha, beta):
    global limit
    if(time.clock() > limit):
        return 0
    go = board.gameover
    cp = board.currentPlayer()
    if(ismax):
        bestScore = -1000000
    else:
        bestScore = 1000000
    bestMove = None
    if(go != 0 and go == cp):
        return bestScore * -1
    elif(go != 0 and go != cp):
        return bestScore
    elif(depthleft <= 0):
        ret = evalFunc(board, board.currentPlayer())
        return ret

    moves = board.generateMoves()
    for move in moves:
        board.playMove(move)
        score = miniMaxFunc(board, evalFunc, depthleft - 1, not ismax, alpha, beta)
        board.undoMove()
        if(ismax):
            bestScore = max(bestScore, score)
            alpha = max(alpha, bestScore)
        else:
            bestScore = min(bestScore, score)
            beta = min(beta, bestScore)
        if(beta <= alpha):
            break
    return bestScore
