import sys

SHORT_NAME = {
    'R': 'Rook',
    'N': 'Knight',
    'B': 'Bishop',
    'Q': 'Queen',
    'K': 'King',
    'P': 'Pawn'
}

class Chess_box(object):
    def __init__(self, chess_type=None, color=None):
        self.chess_type = chess_type
        self.color = color
        if chess_type and color != None:
            self.name = color + ' ' + chess_type
        else:
            self.name = '-'
    def place(self, board):
        ''' Keep a reference to the board '''
        self.board = board
        
class Chess(Chess_box):
    def moves_available(self, pos, orthogonal, diagonal, distance):
        fisrt_move = True
        allowed_moves = []
        orth = ((-1, 0), (0, -1), (0, 1), (1, 0))
        diag = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        piece = self
        begin_pos = pos
        board = self.board.chess_map
        if orthogonal and diagonal:
            directions = diag + orth
        elif diagonal:
            directions = diag
        elif orthogonal:
            directions = orth
        for x, y in directions:
            collision = False
            step = 1
            while step < distance+1:
                if collision: break
                dest = begin_pos[0] + step * x, begin_pos[1] + step * y
                if dest[0] in range(0, 8) and dest[1] in range(0, 8):
                    if board[dest[0]][dest[1]].color == None:
                        allowed_moves.append(dest)
                    elif board[dest[0]][dest[1]].color == self.color:
                        collision = True
                    else:
                        allowed_moves.append(dest)
                        collision = True
                step += 1
        return allowed_moves


class King(Chess):    
    name = 'King'

    def moves_available(self, pos):
        return super(King, self).moves_available(pos, True, True, 1)


class Queen(Chess):


    def moves_available(self, pos):
        return super(Queen, self).moves_available(pos, True, True, 8)


class Rook(Chess):


    def moves_available(self, pos):
        return super(Rook, self).moves_available(pos, True, False, 8)


class Bishop(Chess):


    def moves_available(self, pos):
        return super(Bishop, self).moves_available(pos, False, True, 8)


class Knight(Chess):

    def moves_available(self, pos):
        board = self.board.chess_map
        allowed_moves = []
        begin_pos = pos
        deltas = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for x, y in deltas:
            dest = begin_pos[0] + x, begin_pos[1] + y
            if dest[0] in range(0, 8) and dest[1] in range(0, 8):
                if board[dest[0]][dest[1]].color != self.color:
                        allowed_moves.append(dest)     
        return allowed_moves


class Pawn(Chess):
    def moves_available(self, pos):
        board = self.board.chess_map
        if self.color == 'white':
            self.startpos = 1
            step = 1
            enermy = ['black']
        else:
            self.startpos = 6
            step = -1
            enermy = ['white']
        allowed_moves = []
        # Moving
        begin_pos = pos
        forward = begin_pos[0] + step, begin_pos[1]
        if board[forward[0]][forward[1]].color == None:
            allowed_moves.append(forward)
            
        # Double moves
        if begin_pos[0] == self.startpos:
            double_forward = (forward[0] + step, forward[1])
            if board[forward[0]][forward[1]].color == None:
                allowed_moves.append(double_forward)
                
        # Attacking
        for a in range(-1, 2, 2):
            if begin_pos[1] + a in range(0, 8):
                attack = begin_pos[0] + step, begin_pos[1] + a
                if board[attack[0]][attack[1]].color in enermy:
                    allowed_moves.append(attack)    
        return allowed_moves

def create_piece(chess_type, color):
    if chess_type in (None, '-'):
        chess_box = Chess_box()
        return chess_box       
    color = color
    type = name = chess_type
    module = sys.modules[__name__]
    return module.__dict__[type](name, color)
