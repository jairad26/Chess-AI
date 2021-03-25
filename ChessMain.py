"""
Main driver file handlign user input and displaying GameState object
Mostly pygame focused
"""

import pygame as p

import ChessEngine

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
Responsible for all graphics within current game state
'''

def drawGameState(screen, gs):
    drawBoard(screen) #draws squares on board
    #add in piece highlighting or legal moves
    drawPieces(screen, gs.board) #draw pieces on top of squares
    
'''
draw squares on the board, top left is white always
'''    
def drawBoard(screen):
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
    
    #print(gs.board)
    loadImages() #only do once, before while loop
    running = True
    sqSelected = () #no square selected initially, keep track of last click of user (tuple: (row,col))
    playerClicks = [] #keeps track of player clicks (two tuples: [(6,4),(4,4)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #handles mouse
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x,y) location of mouse
                col = location[0]//SQ_SIZE #to get col, integer divide x coord on board w size of each square 
                row = location[1]//SQ_SIZE #to get row, integer divide y coord on board w size of each square 
                if sqSelected == (row,col): #user clicked same square twice, so unselect
                    spSelected = () #deselect
                    playerClicks = [] #clear player clicks
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected) #append for both 1st and 2nd clicks
                if len(playerClicks) == 2: #after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = () #reset uer clicks
                    playerClicks = []
            #handles keys
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
                    
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
                
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()
        



if __name__ == "__main__":    
    main()