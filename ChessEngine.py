"""
Storing all info abt state of chess board
Determining valid moves
keeps move log
"""

class GameState():
    def __init__(self):
        #8 x 8 list for board
        #represented by 2 char str, first letter is color, and corresponding piece letter
        #-- represents empty space
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wK","wQ","wB","wN","wR"],
        ]
        self.whiteToMove = True
        self.moveLog = []

    
    '''
    Takes move as a parameter, executes it (doesn't work for castling, en passant, pawn promotion)
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log move to undo later or display game
        self.whiteToMove = not self.whiteToMove #next person's turn
        
    '''
    Undo last move
    '''
    def undoMove(self):
        if len(self.moveLog) != 0: #make sure there is a move to undo
           move = self.moveLog.pop()
           self.board[move.startRow][move.startCol] = move.pieceMoved
           self.board[move.endRow][move.endCol] = move.pieceCaptured 
           self.whiteToMove = not self.whiteToMove #prev person's turn
        
class Move():
    #maps keys to values
    #key : value
    ranksToRows = {"1":7,"2":6,"3":5,"4":4,
                   "5":3,"6":2,"7":1,"8":0}
    
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    
    filesToCols = {"a":0,"b":1,"c":2,"d":3,
                   "e":4,"f":5,"g":6,"h":7}
    
    colsToFiles = {v: k for k, v in filesToCols.items()}
    
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        
    def getChessNotation(self):
        #you can add to make this more like chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    