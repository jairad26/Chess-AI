"""
Storing all info abt state of chess board
Determining valid moves
keeps move log
"""
import Move
from Move import Move
import CastlingRights
from CastlingRights import CastlingRights
import copy

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
        
        # self.board = [
        #     ["--","--","--","bQ","bK","--","--","--"],
        #     ["--","--","--","--","--","--","--","--"],
        #     ["--","--","--","--","--","--","--","--"],
        #     ["--","--","--","--","--","--","--","--"],
        #     ["--","--","--","--","--","--","--","--"],
        #     ["--","--","--","--","--","--","--","--"],
        #     ["--","--","--","--","--","--","--","--"],
        #     ["--","--","--","--","wK","--","--","--"],
        # ]
        
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = () # coord for square where en passant capture is possible
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRights = CastlingRights(True, True, True, True)
        self.castleRightsLog = [CastlingRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, 
                                               self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)]

    
    '''
    Takes move as a parameter, executes it (doesn't work for castling, en passant, pawn promotion)
    '''
    def makeMove(self, move):
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.board[move.startRow][move.startCol] = "--"
        self.moveLog.append(move) #log move to undo later or display game
        try:
            if(self.moveLog[-1] == self.moveLog[-5] == self.moveLog[-9]):
                self.staleMate = True
        except(IndexError):
            pass
        #print(self.moveLog)
        self.whiteToMove = not self.whiteToMove #next person's turn
        #update king's position
        # promotionPiece = ''
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
            
        #pawn promotion
        elif move.pieceMoved == 'wP' and move.endRow == 0:
            self.board[move.endRow][move.endCol] = 'wQ'
            # while(promotionPiece == ''):
            #     promotionPiece = input('\n What would you like to promote to? NOTE: You CAN NOT undo a promotion! \n')
            #     if(promotionPiece == 'Q'):
            #         self.board[move.endRow][move.endCol] = 'wQ'
            #     elif(promotionPiece == 'N'):
            #         self.board[move.endRow][move.endCol] = 'wN'
            #     elif(promotionPiece == 'B'):
            #         self.board[move.endRow][move.endCol] = 'wB'
            #     elif(promotionPiece == 'R'):
            #         self.board[move.endRow][move.endCol] = 'wR'
            #     else:
            #         promotionPiece = ''
            #         print('invalid input, try again')
        elif move.pieceMoved == 'bP' and move.endRow == 7:
            move.isPawnPromotion = True
            self.board[move.endRow][move.endCol] = 'bQ'
            # while(promotionPiece == ''):
            #     promotionPiece = input('\n What would you like to promote to? NOTE: You CAN NOT undo a promotion! \n')
            #     if(promotionPiece == 'Q'):
            #         self.board[move.endRow][move.endCol] = 'bQ'
            #     elif(promotionPiece == 'N'):
            #         self.board[move.endRow][move.endCol] = 'bN'
            #     elif(promotionPiece == 'B'):
            #         self.board[move.endRow][move.endCol] = 'bB'
            #     elif(promotionPiece == 'R'):
            #         self.board[move.endRow][move.endCol] = 'bR'
            #     else:
            #         promotionPiece = ''
            #         print('invalid input, try again')
        
        
            
        #update enpassantPossible variable
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2: #only on 2 square pawn advances
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()
        
        #enpassant move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--' #capturing the pawn
            
        #castle move
        if move.isCastleMove:
            if(move.endCol - move.startCol == 2): #kingside castle, since endCol number is 2 more than start col
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1] #moves rook
                self.board[move.endRow][move.endCol+1] = '--' #erase old rook
                # NOTE THIS IS A HUGE ERROR FIX THIS CASTLING STUFF SOON PLS
                # pass
            else: #queenside castle
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = '--'
            
        self.enpassantPossibleLog.append(self.enpassantPossible)
        
        #update castling rights - whenever it is a rook or a king move
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastlingRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, 
                                               self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))
            
        
    '''
    Undo last move
    '''
    def undoMove(self):
        if len(self.moveLog) != 0: #make sure there is a move to undo
            move = self.moveLog.pop()
            
            #undo pawn promotion
            if move.isPawnPromotion:
                allyColor = move.pieceMoved[1]
                self.board[move.startRow][move.startCol] = 'wP' if allyColor == 'w' else 'bP'
                self.board[move.endRow][move.endCol] = move.pieceCaptured
                self.whiteToMove = not self.whiteToMove #prev person's turn
            else:
                self.board[move.startRow][move.startCol] = move.pieceMoved
                self.board[move.endRow][move.endCol] = move.pieceCaptured 
                self.whiteToMove = not self.whiteToMove #prev person's turn
                #update king's position
                if move.pieceMoved == 'wK':
                    self.whiteKingLocation = (move.startRow, move.startCol)
                elif move.pieceMoved == 'bK':
                    self.blackKingLocation = (move.startRow, move.startCol)
                #undo en passant
                if move.isEnpassantMove:
                    self.board[move.endRow][move.endCol] = '--' #leave ending square blank
                    self.board[move.startRow][move.endCol] = move.pieceCaptured
                    # self.enpassantPossible = (move.endRow, move.endCol)
                    if(self.whiteToMove):
                        self.board[move.startRow][move.endCol] = 'bP' #uncapturing the pawn
                    else:
                        self.board[move.startRow][move.endCol] = 'wP' #uncapturing the pawn
                    
                # #undo a 2 square pawn avance
                # if(move.pieceMoved[1] == 'P' and abs(move.startRow-move.endRow)==2):
                #     self.enpassantPossible = ()
                self.enpassantPossibleLog.pop()
                self.enpassantPossible = self.enpassantPossibleLog[-1]    
                #undo castling rights
                self.castleRightsLog.pop() #get rid of new castle rights from the move we are undoing
                #castleRights = copy.deepcopy(self.castleRightsLog[-1])
                castleRights = self.castleRightsLog[-1]
                self.currentCastlingRights = CastlingRights(castleRights.wks, castleRights.bks, castleRights.wqs, castleRights.bqs) #set curr castle rights to the last one in the list
                
                #undo castling move
                if move.isCastleMove:
                    if move.endCol - move.startCol == 2: #kingside
                        self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol-1]
                        self.board[move.endRow][move.endCol - 1] = '--'
                    else: #queenside
                        self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                        self.board[move.endRow][move.endCol+1] = '--'
                    
            
                
            
            
            self.checkMate = False
            self.staleMate = False
            
    '''
    Update castle rights given the move
    '''
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: #left rook
                    self.currentCastlingRights.wqs = False
                elif move.startCol == 7: #right rook
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 7:
                if move.startCol == 0: #left rook
                    self.currentCastlingRights.bqs = False
                elif move.startCol == 7: #right rook
                    self.currentCastlingRights.bks = False
                    
        #if a rook is captured
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRights.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRights.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.bks = False
        
    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        # for log in self.castleRightsLog:
        #     print(log.wks, log.wqs, log.bks, log.bqs, end = ", ")
        moves = []
        tempCastlingRights = CastlingRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, 
                                               self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)
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
                #print(moves)
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
            #print(len(moves))
            if(len(moves) == 0):
                if(self.inCheck):
                    self.checkMate = True
                else:
                    self.staleMate = True
                
        else: #when not in check, all moves are good
            moves = self.getAllPossibleMoves()
            #print(moves)
        #print(moves)
        
        #add castling moves
        if self.whiteToMove:
            allyColor = 'w'
            self.getCastleMoves(kingRow, kingCol, moves, allyColor)
        else:
            allyColor = 'b'
            self.getCastleMoves(kingRow, kingCol, moves, allyColor)
            
        self.currentCastlingRights = tempCastlingRights
        return moves
        
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
        #print(moves)
        return moves           
        
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
        for j in range(len(directions)):
            direction = directions[j]
            possiblePin = () #reset single possible pin
            for i in range(1,8):
                endRow = startRow + direction[0] * i
                endCol = startCol + direction[1] * i
                if(0 <= endRow < 8 and 0 <= endCol < 8):
                    endPiece = self.board[endRow][endCol]
                    if(endPiece[0] == allyColor and endPiece[1] != 'K'):
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, direction[0], direction[1])
                        else: #if possible pin has piece already, this 2nd piece being ally means can't be pinned 
                            break
                    elif(endPiece[0] == enemyColor):
                        type = endPiece[1]
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
                        if(0<= j <= 3 and type == 'R') or \
                            (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'P' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                                    (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == () : #no piece blocking, so check
                                inCheck = True
                                # print(1)
                                # print(type, i, j)
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
                    # print(2)
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks
                                
                        
            
            
    
    
                        
       #ALL TYPES OF PIECES' MOVES START HERE                 
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
                elif(row-1, col-1) == self.enpassantPossible:
                    moves.append(Move((row,col),(row-1,col-1),self.board, isEnpassantMove=True))
                    
                    
            if(col+1 <= 7): #captures to right
                if self.board[row-1][col+1][0] == 'b': #enemy piece to capture
                    if not piecePinned or pinDirection == (-1,1):
                        moves.append(Move((row,col),(row-1,col+1),self.board))
                elif(row-1, col+1) == self.enpassantPossible:
                    moves.append(Move((row,col),(row-1,col+1),self.board, isEnpassantMove=True))
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
                elif(row+1, col-1) == self.enpassantPossible:
                    moves.append(Move((row,col),(row+1,col-1),self.board, isEnpassantMove=True))
            if(col+1 <= 7): #captures to left
                if self.board[row+1][col+1][0] == 'w': #enemy piece to capture
                    if not piecePinned or pinDirection == (1,1):
                        moves.append(Move((row,col),(row+1,col+1),self.board))
                elif(row+1, col+1) == self.enpassantPossible:
                    moves.append(Move((row,col),(row+1,col+1),self.board, isEnpassantMove=True))
                    
                               
    
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
                        
    '''
    Generate all valid castle moves for the king at (row, col) and add to list of moves
    '''                 
    def getCastleMoves(self, row, col, moves, allyColor):
        if self.inCheck:
            return #can't castle while in check
        if(self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingSideCastleMoves(row,col,moves,allyColor)
            # NOTE THIS IS A HUGE ERROR ON CASTLING FIX THIS SOON
            pass
        if(self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQueenSideCastleMoves(row,col,moves,allyColor)
        
    def getKingSideCastleMoves(self, row, col, moves, allyColor):
        if self.board[row][col+1] == '--' and self.board[row][col+2] == '--':
            if not self.squareUnderAttack(row, col+1) and not self.squareUnderAttack(row,col+2):
                moves.append(Move((row,col), (row,col+2),self.board, isCastleMove=True))
    
    def getQueenSideCastleMoves(self,row,col,moves,allyColor):
        if self.board[row][col-1] == '--' and self.board[row][col-2] == '--' and self.board[row][col-3] =='--':
            if not self.squareUnderAttack(row, col-1) and not self.squareUnderAttack(row,col-2):
                moves.append(Move((row,col), (row,col-2),self.board, isCastleMove=True))
    
    def squareUnderAttack(self, row, col):
        self.whiteToMove = not self.whiteToMove #switch to opponent's turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == row and move.endCol == col: #square is under ttack
                return True
        return False
                        
                        
                        
                        
                        
