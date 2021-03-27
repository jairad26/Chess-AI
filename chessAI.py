import random
from tkinter.constants import S

pieceScore = {'K': 0, 'Q': 900, 'R': 500, 'B': 300, 'N': 300, 'P': 100}
checkmateScore = 1000
stalemateScore = 0


'''
helper method to make first recursive call
'''
def findBestMove(gs, validMoves, DEPTH):
    global nextMove, counter
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    # findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove, DEPTH)
    # findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1, DEPTH)
    
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -checkmateScore, checkmateScore, 1 if gs.whiteToMove else -1, DEPTH)
    print(counter)
    return nextMove

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier, DEPTH):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    #move ordering - implement later
    maxScore = -checkmateScore
    for move in validMoves:
        # print(move.pieceMoved, move.startRow, move.startCol, move.endRow, move.endCol)
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier, DEPTH)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha: #pruning happens
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore



'''
min max w recursion
'''
def findMoveMinMax(gs, validMoves, depth, whiteToMove, DEPTH):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    if whiteToMove:
        #trying to maximize
        maxScore = -checkmateScore
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, False, DEPTH)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = checkmateScore
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, True, DEPTH)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore

'''
negamax, recursion
'''
def findMoveNegaMax(gs, validMoves, depth, turnMultiplier, DEPTH):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = -checkmateScore
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier, DEPTH)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore

def findRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]


'''
find best move, min max no recursion
'''    
def findBestMoveMinMaxNoRecursion(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = checkmateScore
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        if gs.staleMate:
            opponentMaxScore = stalemateScore
        elif gs.checkMate:
            opponentMaxScore = -checkmateScore
        else:
            opponentMaxScore = -checkmateScore
            for opponentsMove in opponentsMoves:
                gs.makeMove(opponentsMove)
                gs.getValidMoves()
                if gs.checkMate:
                    score = checkmateScore
                elif gs.staleMate:
                    score = stalemateScore
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove
    


 
 
    
'''
positive score good for white, negative score good for black
'''    
def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -checkmateScore #black wins
        else:
            return checkmateScore #white wins
    elif gs.staleMate:
        return stalemateScore
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
                
    return score    

'''
score the board based on material
'''
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
                
    return score



def orderMoves(gs, validMoves):
    for move in validMoves:
        moveScoreGuess = 0
        if(move.pieceCaptured != "--"):
            moveScoreGuess = 10 * pieceScore[move.pieceCaptured[1]] - pieceScore[move.pieceMoved[1]]
            
        if(move.isPawnPromotion):
            moveScoreGuess += pieceScore['Q']
            