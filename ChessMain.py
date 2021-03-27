"""
Main driver file handlign user input and displaying GameState object
Mostly pygame focused
"""

import pygame as p

import ChessEngine
from tkinter import *
from tkinter import messagebox
import chessAI


WIDTH = 512
HEIGHT = 512
DIMENSION = 8 #dimension of a chess board is 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
Initialize a dictionary of images. Called exactly once in main
Can later be changed to diff images if you want
'''

def loadImages():
    pieces = ['wP', 'wR','wN','wB', 'wK','wQ','bP', 'bR','bN','bB', 'bK','bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #Can access image by saying 'IMAGES[<piece_name>]


'''
Highlights square selected and moves for piece selected
'''
def highlightSquares(screen, gs, validMoves, sqSelected, prevSqSelected, secondPrevSqSelected):
    if sqSelected != ():
        row, col = sqSelected
        if gs.board[row][col][0] == ('w' if gs.whiteToMove else 'b'): #sq selected is a piece that can be moved
            #highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #transparency value -> 0 is transparent, 255 opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (col*SQ_SIZE, row*SQ_SIZE))
            #highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == row and move.startCol == col:
                    screen.blit(s,(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))
    if prevSqSelected != ():
        prevRow, prevCol = prevSqSelected
        secondPrevCol, secondPrevRow = secondPrevSqSelected
        #highlight selected square
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100) #transparency value -> 0 is transparent, 255 opaque
        s.fill(p.Color('red'))
        screen.blit(s, (prevCol*SQ_SIZE, prevRow*SQ_SIZE))
        screen.blit(s, (secondPrevRow*SQ_SIZE, secondPrevCol*SQ_SIZE))
        
   
'''
Responsible for all graphics within current game state
'''
def drawGameState(screen, gs, validMoves, sqSelected, prevSqSelected, secondPrevSqSelected):
    drawBoard(screen) #draws squares on board
    highlightSquares(screen, gs, validMoves, sqSelected, prevSqSelected, secondPrevSqSelected)
    drawPieces(screen, gs.board) #draw pieces on top of squares
    
'''
draw squares on the board, top left is white always
'''    
def drawBoard(screen):
    global colors
    colors = [p.Color(235, 235, 208), p.Color(119, 148, 85)]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = colors[(i+j)%2]
            p.draw.rect(screen,color, p.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
    
'''
draw pieces on the board
''' 
def drawPieces(screen, board):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            piece = board[i][j]
            if piece != "--": #not empty
                screen.blit(IMAGES[piece], p.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                
                
                
'''
Main driver for code, handles input and updating graphic
'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
    animate = False #flag for when to animate
    
    #print(gs.board)
    loadImages() #only do once, before while loop
    running = True
    sqSelected = () #no square selected initially, keep track of last click of user (tuple: (row,col))
    prevSqSelected = ()
    secondPrevSqSelected = ()
    playerClicks = [] #keeps track of player clicks (two tuples: [(6,4),(4,4)])
    gameOver = False
    playerOne = True #if human is playing white,then this will be true. If AI is playing, then false
                     #can also make this an integer value, 0 being human 1-10 being difficulty of AI
    playerTwo = False #Same as above but for black
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #handles mouse
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos() #(x,y) location of mouse
                    col = location[0]//SQ_SIZE #to get col, integer divide x coord on board w size of each square 
                    row = location[1]//SQ_SIZE #to get row, integer divide y coord on board w size of each square 
                    if sqSelected == (row,col): #user clicked same square twice, so unselect
                        sqSelected = () #deselect
                        playerClicks = [] #clear player clicks
                    else:
                        sqSelected = (row,col)
                        playerClicks.append(sqSelected) #append for both 1st and 2nd clicks
                    if len(playerClicks) == 2: #after 2nd click
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                print(move.getChessNotation())
                                moveMade = True
                                animate = True
                                prevSqSelected = playerClicks[-1]
                                secondPrevSqSelected = playerClicks[-2]
                                sqSelected = () #reset uer clicks
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
                            
            #handles keys
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_r: #reset when 'r' is pressed
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    prevSqSelected = ()
                    secondPrevSqSelected = ()
                    moveMade = False
                    gameOver = False
                    animate = False
                    
        #Chess AI
        if not gameOver and not humanTurn:
            AIMove = chessAI.findBestMove(gs, validMoves)
            if AIMove is None:
                AIMove = chessAI.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            print(AIMove.getChessNotation())
            moveMade = True
            animate = True
        
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
                
        #print(prevSqSelected)
        drawGameState(screen,gs, validMoves, sqSelected, prevSqSelected, secondPrevSqSelected)
        
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Draw by stalemate')
        clock.tick(MAX_FPS)
        p.display.flip()
        

'''
animating a move
'''
def animateMove(move, screen, board, clock):
    global colors
    doubleRow = move.endRow - move.startRow
    doubleCol = move.endCol - move.startCol
    framesPerSquare = 2 #frames to move in 1 square
    frameCount = (abs(doubleRow) + abs(doubleCol)) * framesPerSquare
    for frame in range(frameCount + 1):
        row,col = ((move.startRow + doubleRow * frame/frameCount, move.startCol + doubleCol*frame/frameCount))
        drawBoard(screen)
        drawPieces(screen, board)
        #erase the piece from its ending square
        color = colors[(move.endRow+move.endCol)%2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(int(col*SQ_SIZE), int(row*SQ_SIZE), int(SQ_SIZE), int(SQ_SIZE)))
        p.display.flip()
        clock.tick(60)
    
def drawText(screen, text):
    font = p.font.SysFont("Ariel", 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0,0,WIDTH, HEIGHT).move(int(WIDTH/2 - textObject.get_width()/2), int(HEIGHT/2 - textObject.get_height()/2))
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Black"))
    screen.blit(textObject, textLocation.move(2,2))

if __name__ == "__main__":    
    main()