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
            ["--","--","--","--","bP","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wK","wQ","wB","wN","wR"],
        ]
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []

    
    '''
    Takes move as a parameter, executes it (doesn't work for castling, en passant, pawn promotion)
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log move to undo later or display game
        #print(self.moveLog)
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
        
    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves()
    
    '''
    All moves not considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                turn = self.board[i][j][0]
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[i][j][1]
                    self.moveFunctions[piece](i,j,moves) #calls respective function based on piece
        return moves
                        
                        
    '''
    get all the pawn moves for the pawn located at row, col and add these moves to the list
    '''
    def getPawnMoves(self, row, col, moves):
        if self.whiteToMove: #white's turn to move
            if(self.board[row-1][col] == "--"): #when moving "up" the board, row decreases
                moves.append(Move((row,col), (row-1,col),self.board))
                if(row == 6 and self.board[row-2][col] == "--"): #check if can move 2 spaces from starting spot
                    moves.append(Move((row,col),(row-2,col),self.board)) 
            if(col-1 >= 0): #captures to left
                if self.board[row-1][col-1][0] == 'b': #enemy piece to capture
                    moves.append(Move((row,col),(row-1,col-1),self.board))
            if(col+1 <= 7): #captures to right
                if self.board[row-1][col+1][0] == 'b': #enemy piece to capture
                    moves.append(Move((row,col),(row-1,col+1),self.board))
        else:
            if(self.board[row+1][col] == "--"): #when moving "down" the board, row increases
                moves.append(Move((row,col), (row+1,col),self.board))
                if(row == 1 and self.board[row+2][col] == "--"): #check if can move 2 spaces from starting spot
                    moves.append(Move((row,col),(row+2,col),self.board)) 
            if(col-1 >= 0): #captures to right
                if self.board[row+1][col-1][0] == 'w': #enemy piece to capture
                    moves.append(Move((row,col),(row+1,col-1),self.board))
            if(col+1 <= 7): #captures to left
                if self.board[row+1][col+1][0] == 'w': #enemy piece to capture
                    moves.append(Move((row,col),(row+1,col+1),self.board))
                    
        #add promotions later
                               
    
    '''
    get all the rook moves for the rook located at row, col and add these moves to the list
    '''
    def getRookMoves(self, row, col, moves):
        directions = ((-1,0),(0,-1),(1,0),(0,1)) #up, left, down, right
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty space valid
                        moves.append(Move((row,col),(endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #enemy piece valid
                        moves.append(Move((row,col),(endRow,endCol), self.board))
                        break
                    else: #friendly place invalid
                        break
                else: #off board
                    break
    
    '''
    get all the knight moves for the knight located at row, col and add these moves to the list
    '''
    def getKnightMoves(self, row, col, moves):
        knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)) #up, left, down, right
        ally = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = row+m[0]
            endCol = col+m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8: #on board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ally: #when not ally piece, can move there
                    moves.append(Move((row,col),(endRow, endCol), self.board))
    
    '''
    get all the bishop moves for the bishop located at row, col and add these moves to the list
    '''
    def getBishopMoves(self, row, col, moves):
        directions = ((-1,-1),(-1,1),(1,-1),(1,1)) #up, left, down, right
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty space valid
                        moves.append(Move((row,col),(endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #enemy piece valid
                        moves.append(Move((row,col),(endRow,endCol), self.board))
                        break
                    else: #friendly place invalid
                        break
                else: #off brand
                    break
    
    '''
    get all the queen moves for the queen located at row, col and add these moves to the list
    '''
    def getQueenMoves(self, row, col, moves):
        self.getRookMoves(row,col,moves)
        self.getBishopMoves(row,col,moves)
    
    '''
    get all the king moves for the king located at row, col and add these moves to the list
    '''
    def getKingMoves(self, row, col, moves):
        kingMoves = ((-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(0,-1),(1,0),(0,1)) #up, left, down, right
        ally = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = row+kingMoves[i][0]
            endCol = col+kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8: #on board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ally: #when not ally piece, can move there
                    moves.append(Move((row,col),(endRow, endCol), self.board))
    
    
        
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
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    