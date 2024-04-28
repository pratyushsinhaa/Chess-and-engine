''' Driver File Game state and allat'''
class GameState():
    def __init__(self):
        self.board = [
            #First char is the color, second char is the piece name, "--" represents empty space
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        self.moveFunctions ={'p':self.getPawnMoves, 'R': self.getRookMoves, 'Q':self.getQueenMoves,
                             'K':self.getKingMoves, 'B': self.getBishopMoves, 'N':self.getKnightMoves}
        self.WhiteToMove = True
        self.movelog = []
    def makeMove(self, move):
        if move in self.getValidMoves():
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.movelog.append(move)  # log the move to show history or unmove is later
            self.WhiteToMove = not self.WhiteToMove
        else:
            print("Invalid move")
    
            
            
        
    '''UNDO THE LAST MOVE'''
    def undoMove(self):
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
        self.board[move.endRow][move.endCol] = move.pieceCaptured
        self.WhiteToMove = not self.WhiteToMove
        
        
        
    def getValidMoves(self):
        return self.getAllPossibleMoves() # modify and fix this method later on 
    
    
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.WhiteToMove) or (turn == 'b' and not self.WhiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves) # calls appropriate piece move function
        return moves
                        
                        
    
    def getPawnMoves(self,r,c,moves):   # PAWWWWWWNNNN
        if self.WhiteToMove:
            if self.board[r-1][c] == "--": # pawn adavnace by one
                moves.append(Move((r,c),(r-1,c),self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c-1 >=0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1 < 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r,c),(r-1,c+1),self.board))
                    #BLACK PAWN MOVES NOW
        elif not self.WhiteToMove:
            if self.board[r+1][c] == "--": # pawn adavnace by one
                moves.append(Move((r,c),(r+1,c),self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c-1 >=0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1 < 7:
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c+1),self.board))
                
                

    def getRookMoves(self,r,c,moves): #ROOOOOOK
        directions = ((-1,0),(0,-1),(1,0),(0,1))
        enemyColor = "b" if self.WhiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i 
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c),(endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] != enemyColor:  # FRIENDLY PIECE
                        break
                    else: # OFF THE BOARD 
                        break
                else:
                    break
                    
    
    
    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)




    def getKingMoves(self,r,c,moves):
       kingMoves = ((-1,1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1))
       allyColor = "w" if self.WhiteToMove else "b"
       for i in range(8):
           endRow = r + kingMoves[i][0]
           endCol = c + kingMoves[i][1]
           if 0 <= endRow < 8 and 0 <= endCol <= 8:
               endPiece = self.board[endRow][endCol]
               if endPiece[0] != allyColor:
                   moves.append(Move((r,c), (endRow, endCol), self.board))




    def getBishopMoves(self,r,c,moves):
        directions = ((-1,-1),(-1,1),(1,-1),(1,1))
        enemyColor = "b" if self.WhiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i 
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c),(endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] != enemyColor:  # FRIENDLY PIECE
                        break
                    else: # OFF THE BOARD 
                        break
                else:
                    break




    def getKnightMoves(self,r,c,moves):
       knightMoves = ((-2,-1),(-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))
       allyColor = "w" if self.WhiteToMove else "b"
       for m in knightMoves:
           endRow = r + m[0]
           endCol = c + m[1]
           if 0 <= endRow < 8 and 0 <= endCol <8:
               endPiece = self.board[endRow][endCol]
               if endPiece[0] != allyColor:
                   moves.append(Move((r,c), (endRow, endCol), self.board))
               





class Move(): 
    
    rankstoRows = {"1":7, "2":6, "3":5, "4":4,
                   "5":3, "6":2, "7": 1, "8":0}
    rowstoRanks = {v: k for k, v in rankstoRows.items()}
    
    filestoCols = {"h":7, "g":6, "f":5, "e":4,
                   "d":3, "c":2, "b": 1, "a":0}
    colsToFiles = {v: k for k, v in filestoCols.items()}
    
    def __init__(self,startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        
        
        
    def __eq__(self,other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        
    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
        
    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowstoRanks[r]
    