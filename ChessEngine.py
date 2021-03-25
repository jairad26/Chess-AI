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
            ["wR","wN","wB","wQ","wK","wB","wN","wR"],
        ]
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.inCheck = False
        self.pins = []
        self.checks = []

    
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
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        
        if self.inCheck:
            if len(self.checks) == 1: #if only 1 check, look for blocks
                moves = self.getAllPossibleMoves()
                #to block a check, must move piece into square between enemy piece and king
                check = self.checks[0] # get check info
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol] #check enemy piece checking
                #check checking check check, check check, check  check check checking check
                validSquares = [] #possible squares
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1,8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i) #check[2] and check[3] are check direcctions
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol: #once you get to piece end checks
                            break
                #get rid of any moves that don't block check or move king
                for i in range(len(moves)-1,-1,-1): #go through backwards when removing from a list as iterating
                    if(moves[i].pieceMoved[1] != 'K'): #move doesn't move king so it must block or capture
                        if not (moves[i].endRow, moves[i].endCol) in validSquares: #move doesn't block check or capture piece
                            moves.remove(moves[i])
            else: #double check, so king has to move
                self.getKingMoves(kingRow, kingCol, moves)
        else: #when not in check, all moves are good
            self.getAllPossibleMoves()
                    
        
    '''
    Looks for all possible pins and checks on king
    '''
    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1] 
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        
        #check out in all 8 directions for pins and checks, add pin to list
        directions = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
        for i in range(len(directions)):
            direction = directions[i]
            possiblePin = () #reset single possible pin
            for j in range(1,8):
                endRow = startRow + direction[0] * j
                endCol = startCol + direction[1] * j
                if(0 <= endRow < 8 and 0 <= endCol < 8):
                    endPiece = self.board[endRow][endCol]
                    if(endPiece[0] == allyColor and endPiece[1] != 'K'):
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, direction[0], direction[1])
                        else: #if possible pin has piece already, this 2nd piece being ally means can't be pinned 
                            break
                    elif(endPiece[0] == enemyColor):
                        pieceType = endPiece[1]
                        #there are 5 possibilities in conditional to get check
                        #1.) horizontally  away from king and piece is a rook
                        #2.) diagonally away from king, piece is bishop
                        #3.) 1 square diagonally away, piece is pawn
                        #4.) combine 1.) & 2.), and piece is a queen
                        #5.) any direction 1 square away, piece is king. (used to prevent 2 kings being next to each other
                        
                        #if first 4 directions (orthogonal) and rook, it's check
                        #if last 4 directions (diagonal) and bishop, it's check
                        #if one square away and pawn, check to see if it is going correct direction
                            #white pieces move up the board, black pieces move down the board
                        if(0<= i <= 3 and type == 'R') or \
                            (4 <= i <= 7 and type == 'B') or \
                                (j == 1 and type == 'P' and ((enemyColor == 'w' and 6 <= i <= 7) or (enemyColor == 'b' and 4 <= i <= 5))) or \
                                    (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == () : #no piece blocking, so check
                                inCheck = True
                                checks.append((endRow, endCol, direction[0], direction[1]))
                                break
                            else: #piece blocking so pin
                                pins.append(possiblePin)
                                break
                        else: #enemy piece not applying check
                            break
                else: #off board
                    break
        #check for knight checks
        knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)) #up, left, down, right
        for m in knightMoves:
            endRow = startRow+m[0]
            endCol = startCol+m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8: #on board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N': #enemy knight attacking king
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks
                                
                        
            
            
    
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
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if(self.pins[i][0] == row and self.pins[i][1] == col):
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        if self.whiteToMove: #white's turn to move
            if(self.board[row-1][col] == "--"): #when moving "up" the board, row decreases
                if not piecePinned or pinDirection == (-1,0):
                    moves.append(Move((row,col), (row-1,col),self.board))
                    if(row == 6 and self.board[row-2][col] == "--"): #check if can move 2 spaces from starting spot
                        moves.append(Move((row,col),(row-2,col),self.board)) 
            #captures
            if(col-1 >= 0): #captures to left
                if self.board[row-1][col-1][0] == 'b': #enemy piece to capture
                    if not piecePinned or pinDirection == (-1,-1):
                        moves.append(Move((row,col),(row-1,col-1),self.board))
            if(col+1 <= 7): #captures to right
                if self.board[row-1][col+1][0] == 'b': #enemy piece to capture
                    if not piecePinned or pinDirection == (-1,1):
                        moves.append(Move((row,col),(row-1,col+1),self.board))
        else:
            if(self.board[row+1][col] == "--"): #when moving "down" the board, row increases
                if not piecePinned or pinDirection == (1,0):
                    moves.append(Move((row,col), (row+1,col),self.board))
                    if(row == 1 and self.board[row+2][col] == "--"): #check if can move 2 spaces from starting spot
                        moves.append(Move((row,col),(row+2,col),self.board)) 
            if(col-1 >= 0): #captures to right
                if self.board[row+1][col-1][0] == 'w': #enemy piece to capture
                    if not piecePinned or pinDirection == (1,-1):
                        moves.append(Move((row,col),(row+1,col-1),self.board))
            if(col+1 <= 7): #captures to left
                if self.board[row+1][col+1][0] == 'w': #enemy piece to capture
                    if not piecePinned or pinDirection == (1,1):
                        moves.append(Move((row,col),(row+1,col+1),self.board))
                    
        #add promotions later
                               
    
    '''
    get all the rook moves for the rook located at row, col and add these moves to the list
    '''
    def getRookMoves(self, row, col, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if(self.pins[i][0] == row and self.pins[i][1] == col):
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][1] != 'Q': #can't remove queen from pin on rook moves, only remove it on bishop moves, b/c getQueenMoves calls getRookMoves
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1,0),(0,-1),(1,0),(0,1)) #up, left, down, right
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #on board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]): #since rooks can move both "up" and "down" the board, must account for all 4 directions
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
        piecePinned = False
        for i in range(len(self.pins)-1,-1,-1):
            if(self.pins[i][0] == row and self.pins[i][1] == col):
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)) #up, left, down, right
        ally = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = row+m[0]
            endCol = col+m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8: #on board
                if not piecePinned: #don't need pin direction b/c no matter what, the knight being pinned can't capture the piece pinning it
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != ally: #when not ally piece, can move there
                        moves.append(Move((row,col),(endRow, endCol), self.board))
    
    '''
    get all the bishop moves for the bishop located at row, col and add these moves to the list
    '''
    def getBishopMoves(self, row, col, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if(self.pins[i][0] == row and self.pins[i][1] == col):
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][1] != 'Q': #can't remove queen from pin on rook moves, only remove it on bishop moves, b/c getQueenMoves calls getRookMoves
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1,-1),(-1,1),(1,-1),(1,1)) #up, left, down, right
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #on board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]): #see rook explanation
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
        rowMoves = (-1,-1,-1, 0,0, 1,1,1) #split to put into KingLocation variables
        colMoves = (-1, 0, 1,-1,1,-1,0,1)
        #read those ^^ vertically, to get each of the directions
        allyColor = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = row+rowMoves[i]
            endCol = col+colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8: #on board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #when not ally piece, can move there
                    #place king on end square and check for checks
                    if(allyColor == 'w'):
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck: 
                        moves.append(Move((row,col),(endRow, endCol), self.board))
                    #place king back on original location
                    if allyColor == 'w':
                        self.whiteKingLocation = (row, col)
                    else:
                        self.blackKingLocation = (row,col)
                        
    
    
        
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
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    