class Move():
    #maps keys to values
    #key : value
    ranksToRows = {"1":7,"2":6,"3":5,"4":4,
                   "5":3,"6":2,"7":1,"8":0}
    
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    
    filesToCols = {"a":0,"b":1,"c":2,"d":3,
                   "e":4,"f":5,"g":6,"h":7}
    
    colsToFiles = {v: k for k, v in filesToCols.items()}
    
    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        
        self.isEnpassantMove = isEnpassantMove
        
        self.isCastleMove = isCastleMove
        
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol*1 #kinda like masking, every move has a unique ID based on number in that pos
        
        
    '''
    Overriding equals method
    '''
    def __eq__(self,other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
        
    def getChessNotation(self):
        #you can add to make this more like chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]