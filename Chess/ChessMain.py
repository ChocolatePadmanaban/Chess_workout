"""
This is our main driver file. It will be responsible for handling user input and displaying the current GameState object
"""

import pygame as p 
from Chess import ChessEngine

WIDTH=HEIGHT=512
DIMENSIONS=8
SQ_SIZE=HEIGHT //DIMENSIONS
MAX_FPS= 15
IMAGES={}



def loadImages():
    """
    Initialize a global dictionary of images. This will be called exactly once int the main
    """
    pieces = ['wp','wR','wN','wB','wK','wQ','bp','bR','bN','bB','bK','bQ']
    for piece in pieces:
        IMAGES[piece]= p.transform.scale( p.image.load('images/'+piece+'.png'), (SQ_SIZE,SQ_SIZE))
    # Note: we can access an image by saying 'IMAGES['wp']'

def main():
    """
    The main driver for our code. this will handle user input and updating the graphics 
    """
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    loadImages() #only do this once, before the while loop 
    running=True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    """
    Responsible for all the graphics within a current game state.
    """
    drawBoard(screen)# draw squares on the board 
    # add in piece highlighting or move suggestion (later)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    """
    Draw the squares on the board 
    """
    global colors
    colors = [p.Color('white'), p.Color('gray')]
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            color = colors[((r+c)%2)]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))


def drawPieces(screen,board):
    """
    Draw the pieces on the board using the current GameState.board 
    """
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = board[r][c]
            if piece != '--' : #not empty squares
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))





if __name__=="__main__":
    main()