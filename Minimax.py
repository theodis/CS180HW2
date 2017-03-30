from Game import Game

def miniMax(board, evalFunc, maxdepth):
    bestMove = None
    bestScore = -1000001
    moves = board.generateMoves()
    for move in moves:
        print(move)
        board.playMove(move)
        score = miniMaxFunc(board, evalFunc, maxdepth, False, -1000000, 1000000)
        print(score)
        if(score > bestScore):
            bestScore = score
            bestMove = move
        board.undoMove()
        print(bestMove)
    return bestMove

def miniMaxFunc(board, evalFunc, depthleft, ismax, alpha, beta):
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
