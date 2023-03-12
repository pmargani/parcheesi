
from Constants import *

# one of four corners
# start (safe) - 1
# 2, 3, 4, 5
# (safe) - 6
# 7, 8, 9, 10, 11, 12
# (safe) - 13
# 13, 14, 15, 16
# start the new corner

# so the board edges are 4*16 long,
# with each player starting at base every 16 positions.
# And base starts at corner + 5
# after a plyaer has gone 4*16  - 5positions, they go up
# a home path till they get home.

# how to denote positions?  Relative to start is easy for each
# piece, but makes it hard to compare pieces from different
# players.  Instead, make absolute position primary, 
# with functions for relative position to base.

# all pieces from all players can share the same home path, so those
# will be positions > 4*16 (64)

# this means for all players but player 1, their absolute position
# will wrap around 0.  So, for player 2, they start at 16 + 5.  When 
# they get past 4*16, they restart at zero, which will be relative
# position 3*16.


#              0 (Player 1 turns into home)
#
#         5 (Player 1 start)  60
#
#      12                    53 (Player 4 start)
# 16                               48 (Player 4 turns into home)
#      21  (Player 2 start)  44
#
#          28     37 (Player 3 start)
#              32 (Player 3 turns into home)
#

# So, once any pleyaer gets past pos. 64, they restart at 0.
# once player gets past start position - 5, they jump to position 64,
# all sharing the same home path.

class Board:
    
    """
    This class is a simple wrapper around a representation of the
    Parchessi board.
    This representation is simply a dictionary where the keys are positions,
    as described above.
    Entries are only necessary if the positions are occupied by a piece.
    Each entry is a list of the Piece objects on that position.
    This class makes it easier to figure out how pieces interact on
    the board.  The actual navigation on the board is handled internally
    by the Piece class.
    """

    def __init__(self):

        # internal representation of the board
        self.board = {}


    def update(self, piece, oldPos, newPos):
        """
        Move piece from old position to new position,
        removing knocked out pieces where appropriate
        """
        if oldPos in self.board:
            # find piece and remove it
            for i, pc in enumerate(self.board[oldPos]):
                if pc == piece:
                    self.board[oldPos].pop(i)
        if newPos not in self.board:
            self.board[newPos] = []
        elif len(self.board[newPos]) > 0 and newPos < BOARDLENGTH and newPos not in SAFE_POSITIONS:
            # there's other pieces here?  Any from other team?
            # TBF: arbitrarly pick first one
            otherPiece = self.board[newPos][0]
            if otherPiece.player.id != piece.player.id:
                # back to base!
                # print("Kill by %s on %s" % (piece, otherPiece))
                otherPiece.deaths += 1
                otherPiece.position = BASE
                self.board[newPos].pop(0)
                piece.kills += 1


        self.board[newPos].append(piece)

    def movePieceToStart(self, piece):
        "update internal representation of board"    
        if piece.startPosition not in self.board:
            self.board[piece.startPosition] = []
        self.board[piece.startPosition].append(piece) 

    def removeFromBoard(self, piece):
        "remove the given piece from the board"
        if piece.position not in self.board:
            print("ERROR: board does not have piece at position %s" % piece.position)
            return
        pcs = self.board[piece.position]
        for i, pc in enumerate(pcs):
            if pc == piece:
                pcs.pop(i)
                break

    def isStartOpen(self, player):    
        "Can the given player place a piece at start?"
        pos = player.startPosition
        if pos not in self.board:
            # it's empty!
            return True
        elif len(self.board[pos]) < 2:
            # just one piece there!
            return True
        else:
            # it's full!
            return False

    def numPiecesOnBoardPos(self, pos, piece):
        "How many pieces on the board's given position?"
        if pos not in self.board:
            return 0
        if pos <= BOARDLENGTH:    
            return len(self.board[pos])
        elif pos >= HOME:
            # act like nobodies there, since there aren't restrictions
            return 0    
        else:
            # treat the home path as four separate paths
            return len([ pc for pc in self.board[pos] if pc.player.id == piece.player.id])    
     
    def numPiecesOnBoard(self):
        "whatever is represented on the board"
        N = 0
        for pos , pcs in self.board.items(): 
            N += len(pcs)
        return N
            
    def isOccupiedByPlayer(self, newPos, player):
        """
        This function ignores the number of pieces actuall at the newPos.
        If one of the pieces belongs to this player it will return True
        """
        result = False
        if newPos not in self.board:
            # no piece is on this position of the self.board
            return result
        pcs = self.board[newPos]
        for pc in pcs:
            if pc.player == player:
                result = True
                break
        return result

    def isOccupiedByOtherPlayer(self, newPos, player):
        """
        This function ignores the number of pieces actually at the newPos.
        If one of the pieces belongs to other player it will return True
        """
        result = False
        if newPos not in self.board:
            # no piece is on this position of the self.board
            return result
        pcs = self.board[newPos]
        for pc in pcs:
            if pc.player != player:
                result = True
                break
        return result

    def printBoard(self, players):
        "Use ascii art to represent 1 base + 64 positions + 8 home path + 1 home for each piece"

        # TBF: this does not use the board dict!
        # but each piece knows where it is, so this works
        numCols = (len(players)*4) + 3
        print("*"*numCols)
        positions = range(BASE, HOME+1)
        for pos in positions:
            s = "%02d " % pos
            for p in players:
                for pc in p.pieces:
                    if pc.position == pos:
                        s += "%s" % pc.id
                    else:
                        s += " "
            print(s)
        print("*"*numCols)      