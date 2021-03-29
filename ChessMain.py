"""
Main driver file handlign user input and displaying GameState object
Mostly pygame focused
"""

import pygame as p

import ChessEngine
from tkinter import *
from tkinter import messagebox
import chessAI


BOARD_WIDTH = 512
BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8 #dimension of a chess board is 8x8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
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
Responsible for all graphics within current game state
'''
def drawGameState(screen, gs, validMoves, sqSelected, prevSqSelected, secondPrevSqSelected, moveLogFont):
    drawBoard(screen) #draws squares on board
    highlightSquares(screen, gs, validMoves, sqSelected, prevSqSelected, secondPrevSqSelected)
    drawPieces(screen, gs.board) #draw pieces on top of squares
    drawMoveLog(screen, gs, moveLogFont)
    
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
draw pieces on the board
''' 
def drawPieces(screen, board):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            piece = board[i][j]
            if piece != "--": #not empty
                screen.blit(IMAGES[piece], p.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                
'''
draws move log in chess notation
'''
def drawMoveLog(screen, gs, font):
    screenNum = 0
    moveLogRect = p.Rect(BOARD_WIDTH, 0 , MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = moveLog
    padding = 5
    nextLinePadding = 10
    
    titleText = 'MOVE LOG'
    
    subtitleTextWhite = 'WHITE'
    subtitleTextBlack = 'BLACK'
    
    titleFont = p.font.SysFont("Arial", 24, False, False)
    subtitleFont = p.font.SysFont("Arial", 18, False, False)
    
    
    titleTextLocation = moveLogRect.move(MOVE_LOG_PANEL_WIDTH // 4, 5)
    titleTextObject = titleFont.render(titleText, True, p.Color('white'))
    screen.blit(titleTextObject, titleTextLocation)
    
    subtitleTextLocationWhite = moveLogRect.move(MOVE_LOG_PANEL_WIDTH // 8, 35)
    subtitleTextLocationBlack = moveLogRect.move(2 * MOVE_LOG_PANEL_WIDTH // 3 - 10, 35)
    subtitleTextObjectWhite = subtitleFont.render(subtitleTextWhite, True, p.Color('white'))
    subtitleTextObjectBlack = subtitleFont.render(subtitleTextBlack, True, p.Color('white'))
    screen.blit(subtitleTextObjectWhite, subtitleTextLocationWhite)
    screen.blit(subtitleTextObjectBlack, subtitleTextLocationBlack)
    
    for i in range(len(moveTexts)):
        if((i//2+1) % 24 == 0):
            screenNum += 1
            p.draw.rect(screen, p.Color("black"), moveLogRect)
            padding = 5
            nextLinePadding = 10
            
            titleText = 'MOVE LOG'
            
            subtitleTextWhite = 'WHITE'
            subtitleTextBlack = 'BLACK'
            
            titleFont = p.font.SysFont("Arial", 24, False, False)
            subtitleFont = p.font.SysFont("Arial", 18, False, False)
            
            
            titleTextLocation = moveLogRect.move(MOVE_LOG_PANEL_WIDTH // 4, 5)
            titleTextObject = titleFont.render(titleText, True, p.Color('white'))
            screen.blit(titleTextObject, titleTextLocation)
            
            subtitleTextLocationWhite = moveLogRect.move(MOVE_LOG_PANEL_WIDTH // 8, 35)
            subtitleTextLocationBlack = moveLogRect.move(2 * MOVE_LOG_PANEL_WIDTH // 3 - 10, 35)
            subtitleTextObjectWhite = subtitleFont.render(subtitleTextWhite, True, p.Color('white'))
            subtitleTextObjectBlack = subtitleFont.render(subtitleTextBlack, True, p.Color('white'))
            screen.blit(subtitleTextObjectWhite, subtitleTextLocationWhite)
            screen.blit(subtitleTextObjectBlack, subtitleTextLocationBlack)
            
            
        text = str(moveTexts[i])
        textObject = font.render(text, True, p.Color('white'))
        if(i % 2 == 0):
            moveNumText = str(i//2 + 1) + '.'
            
            moveNumTextObject = font.render(moveNumText, True, p.Color('white'))
            moveNumTextLocation = moveLogRect.move(5, 55 + padding + (i%46)*nextLinePadding)
            screen.blit(moveNumTextObject, moveNumTextLocation)
            textLocation = moveLogRect.move(MOVE_LOG_PANEL_WIDTH // 8 + 10, 55 + padding + (i%46)*nextLinePadding)
        else:
            textLocation = moveLogRect.move(2 * MOVE_LOG_PANEL_WIDTH // 3 - 10 + 10, 55 + padding + ((i%46)-1)*nextLinePadding)
        
        screen.blit(textObject, textLocation)

                
                
'''
Main driver for code, handles input and updating graphic
'''

def main():
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH+MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Arial", 12, False, False)
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
    playerOne = -1 #if human is playing white,then this will be true. If AI is playing, then false
                     #can also make this an integer value, 0 being human 1-10 being difficulty of AI
    playerTwo = -1 #Same as above but for black
    while running:
        humanTurn = (gs.whiteToMove and playerOne == -1) or (not gs.whiteToMove and playerTwo == -1)
        
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #handles mouse
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos() #(x,y) location of mouse
                    col = location[0]//SQ_SIZE #to get col, integer divide x coord on board w size of each square 
                    row = location[1]//SQ_SIZE #to get row, integer divide y coord on board w size of each square 
                    if sqSelected == (row,col) or col >= 8: #user clicked same square twice, so unselect or user clicked mouse log
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
                                print(str(gs.moveLog[-1]))
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
            if gs.whiteToMove:
                AIMove = chessAI.findBestMove(gs, validMoves, playerOne)
            else:
                AIMove = chessAI.findBestMove(gs, validMoves, playerTwo)
            if AIMove is None:
                if(len(validMoves) != 0):
                    AIMove = chessAI.findRandomMove(validMoves)
                else:
                    break
            gs.makeMove(AIMove)
            print(str(gs.moveLog[-1]))
            moveMade = True
            animate = True
        
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
                
        #print(prevSqSelected)
        drawGameState(screen,gs, validMoves, sqSelected, prevSqSelected, secondPrevSqSelected, moveLogFont)
        
        if gs.checkMate or gs.staleMate:
            gameOver = True
            text = 'Draw by stalemate' if gs.staleMate else ('Black wins by checkmate' if gs.whiteToMove else 'White wins by checkmate')
            drawEndGameText(screen, text)
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
    
def drawEndGameText(screen, text):
    font = p.font.SysFont("Ariel", 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0,0,BOARD_WIDTH, BOARD_HEIGHT).move(int(BOARD_WIDTH/2 - textObject.get_width()/2), int(BOARD_HEIGHT/2 - textObject.get_height()/2))
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Black"))
    screen.blit(textObject, textLocation.move(2,2))

if __name__ == "__main__":    
    main()