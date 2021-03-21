"""
This Class is responsible for storing all the information about the current state of a chess game. It is will be also be 
responsible for determining the valid moves at the current state. It will also keep a move log 
"""
class GameState():
    def __init__ (self):
        """
        board is an 8x8 2d list, each element of the list has 2 characters.
        The First character represtents the color of the piece, 'b' or 'w'
        The Second character represents the type of the piece, 'K' , 'Q', 'R', 'B','N' or 'P'
        '--' represents an empty space with no piece
        """
        self.board = [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bp','bp','bp','bp','bp','bp','bp','bp'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['wp','wp','wp','wp','wp','wp','wp','wp'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR']
        ]

        self.moveFunctions = {'p': self.getPawnMoves,'K': self.getKingMoves,'N':self.getKnightMoves,
        'R': self.getRookMoves,'Q':self.getQueenMoves,'B': self.getQueenMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation=(7,4)
        self.blackKingLocation=(0,4)
        self.checkMate = False
        self.stalemate = False

    def makeMove(self, move):
        """
        Takes a Move as a parameter and executes it (this will not work for casling, pawn promotion and en-passant)
        """
        self.board[move.startRow][move.startCol]= '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)# log the move so we can undo it later 
        self.whiteToMove = not self.whiteToMove # swap players
        # update the king's location if moved 
        if move.pieceMoved == 'wK':
            self.whiteKingLocation= (move.endRow,move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation =  (move.endRow,move.endCol)
        
    
    def undoMove(self):
        """
        Undo the last Move made
        """
        if len(self.moveLog) != 0 : #make sure ther is a move to undo 
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #switch turns back
            #update kings position 
            if move.pieceMoved == 'wK':
                self.whiteKingLocation= (move.startRow,move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation =  (move.startRow,move.startCol)
    
    def getValidMoves(self):
        """
        ALL moves considering checks
        """
        # 1. ) generate all possible moves 
        moves = self.getAllPossibleMoves()
        # 2. ) for each move , make the move 
        for i in range(len(moves)-1,-1,-1):
            self.makeMove(moves[i])
            # 3. ) generate all opponent's move 
            # 4. ) for each of your opponent's moves , see if they attack your king 
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i]) # 5. ) if they do attack your kin, not a valid move  
            self.whiteToMove = not self.whiteToMove
            self.undoMove() 
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate= True
            else :
                self.stalemate=True
        else:
            self.checkMate = False
            self.stalemate = False
        return moves 
    
    def inCheck(self):
        """
        Determine if the current player is in check  
        """
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])
    
    def squareUnderAttack(self,r,c):
        """
        Determnin if the enemy can attack the square r, c
        """
        self.whiteToMove = not self.whiteToMove # switch to oppononent's turn 
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True 
        return False


    def getAllPossibleMoves(self):
        """
        All moves with out considering checks 
        """
        moves = []
        for r in range(len(self.board)): # number of rows 
            for c in range(len(self.board[r])):# numbers of colums 
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
        
        return moves
    
    def getPawnMoves(self, r ,c , moves):
        """
        Get all the pawn moves for the pawn located at row, col and add those moves to the list 
        """
        if self.whiteToMove: #white pawn moves 
            if self.board[r-1][c]=='--': #1 square pawn advance 
                moves.append(Move((r,c), (r-1,c),self.board))
                if r==6 and self.board[r-2][c]== '--': #2 square advance 
                    moves.append(Move((r,c),(r-2,c),self.board) )
            if c-1 >=0:
                if self.board[r-1][c-1][0] == 'b': #enemy piece to capture 
                    moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1 <=7: # captures the right
                if self.board[r-1][c+1][0]=='b':
                    moves.append(Move((r,c), (r-1,c+1), self.board))
        else: #black pawn moves
            if self.board[r+1][c]=='--': # 1 square move 
                moves.append(Move((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+2][c]=='--': # 2 square moves 
                    moves.append(Move((r,c),(r+2,c),self.board))
            # Captures
            if c - 1 >=0:  # capture left 
                if self.board[r+1][c-1][0]=='w':
                    moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1 <= 7: # capture right 
                if self.board[r+1][c+1][0]=='w':
                    moves.append(Move((r,c),(r+1,1+c),self.board))
        # add pawn promotions later

    
    def getRookMoves(self, r ,c , moves):
        """
        Get all the rook moves for the pawn located at row, col and add those moves to the list 
        """
        directions = ((-1,0),(0,-1),(1,0),(0,1)) # up , left ,down , right
        enemyColor= 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = r+d[0]*i
                endCol = c+d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8 : #on board 
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--': # empty space valid 
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0] == enemyColor: # enemy piece valid 
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else: # friendly piece invalid 
                        break
                else:
                    break



    def getBishopMoves(self, r ,c , moves):
        """
        Get all the rook moves for the pawn located at row, col and add those moves to the list 
        """
        directions = ((-1,-1),(-1,1),(1,-1),(1,1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow=r+d[0]*i
                endCol=c+d[1]*i
                if 0<= endRow < 8 and 0<= endCol< 8:
                    endPiece=self.board[endRow][endCol]
                    if endPiece == '--': # empty space
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0]== enemyColor: # capture 
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else: # friendly piece invalid 
                        break
                else:
                    break
                

    def getKnightMoves(self, r ,c , moves):
        """
        Get all the rook moves for the pawn located at row, col and add those moves to the list 
        """
        knightMoves= ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0<= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # not an ally piece (empty or enemy piece)
                    moves.append(Move((r,c),(endRow,endCol),self.board))

    def getKingMoves(self, r ,c , moves):
        """
        Get all the rook moves for the pawn located at row, col and add those moves to the list 
        """
        kingMoves=((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,-1))
        allyColor= 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow= r+kingMoves[i][0]
            endCol= c+kingMoves[i][1]
            if 0<= endRow < 8 and 0<= endCol <8:
                endPiece= self.board[endRow][endCol]
                if endPiece[0] != allyColor: # not and ally piece (empty or enemy piece)
                    moves.append(Move((r,c),(endRow,endCol),self.board))


    def getQueenMoves(self, r ,c , moves):
        """
        Get all the rook moves for the pawn located at row, col and add those moves to the list 
        """
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)
    


        

class Move():
    # maps keys to values
    # keys : value
    ranksToRows = {'1':7,'2':6,'3':5,'4':4,'5':3,'6':2,'7':1,'8':0}
    rowsToRank = { v:k for k, v in ranksToRows.items()}
    filesToCols = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
    colsToFiles = {v:k for k,v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000 +self.startCol *100 + self.endRow*10 + self.endCol


    def __eq__(self,other):
        """
        Overriding the Equals method 
        """
        
        if isinstance (other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        #you can add to make this real chess notation 
        return self.getRankFile(self.startRow,self.startCol)+ self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self,r,c):
        return self.colsToFiles[c]+self.rowsToRank[r]
    