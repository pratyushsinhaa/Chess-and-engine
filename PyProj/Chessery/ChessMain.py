'''state info stored here'''

import pygame as p
import ChessEngine


WIDTH = HEIGHT = 512 # 400 IS ALSO A GOOD OPTION
DIMENSION = 8  # BORADS ARE 8X8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
initialize a global dictionary for images
'''
def LoadImages():
    pieces = ['wp','wR','wN','wB','wK','wQ','bp','bR','bN','bB','bK','bQ']
    for piece in pieces:
           IMAGES[piece] = p.transform.scale(p.image.load("images/"+ piece + ".png"), (SQ_SIZE,SQ_SIZE))
        # access images by saying IMAGES['wp]
        

''' MAIN DRIVER FOR CODE, HANDLE INPUT AND GRAPHIC UPDATES'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # flag var for when a move is made
    
    LoadImages()
    running = True
    sqSelected = () # no square is sleected
    playerClicks = [] # keep track of player clicks
    while running:
        for e in p.event.get():
            if e.type ==  p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x,y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row,col):
                    sqSelected = () # DESELECTING A SQUARE 
                    playerClicks = []
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected) # tracking all moves
                    # was that user's second click?
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        moveMade = True
                        gs.makeMove(move)
                        sqSelected = () # reser user clicks
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]
                #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    print("Piece Unmoved back!!")
                    moveMade = True
                    
                    
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

                
        drawGameState(screen, gs)  # Add this line
        clock.tick(MAX_FPS)
        p.display.flip()
        
def drawGameState(screen,gs):
    drawBoard(screen) # draw squares on the baor
    drawPieces(screen,gs.board) #draw pieces on top of those squares
    
        
        
def drawBoard(screen):
    colors = [p.Color("light gray"), p.Color("dark gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        

        
if __name__ == "__main__":
    main()