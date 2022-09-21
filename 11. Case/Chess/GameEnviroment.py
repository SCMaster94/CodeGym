import tkinter as tk
from tkinter import ttk
import ChessMan as cm
from copy import deepcopy

class Board(dict):
    y_axis = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
    x_axis = (1, 2, 3, 4, 5, 6, 7, 8)
    chess_man_die = {'white': [], 'black': []}
    player_turn = None
    halfmove_clock = 0
    fullmove_number = 1
    history = []
    chess_map = []
    def __init__(self, pat=None):
        self.chess_map = []

    def is_in_check_after_move(self, p1, p2):
        tmp = deepcopy(self)
        tmp.move(p1, p2)
        return tmp.king_in_check(self[p1].color)

    def shift(self, p1, p2):
        p1, p2 = p1.upper(), p2.upper()
        piece = self[p1]
        try:
            dest = self[p2]
        except:
            dest = None
        if self.player_turn != piece.color:
            raise NotYourTurn("Not " + piece.color + "'s turn!")
        enemy = ('white' if piece.color == 'black' else 'black')
        moves_available = piece.moves_available(p1)
        if p2 not in moves_available:
            raise InvalidMove
        if self.all_moves_available(enemy):
            if self.is_in_check_after_move(p1, p2):
                raise Check
        if not moves_available and self.king_in_check(piece.color):
            raise CheckMate
        elif not moves_available:
            raise Draw
        else:
            self.move(p1, p2)
            self.complete_move(piece, dest, p1, p2)

    def move(self, p1, p2):
        piece = self[p1]
        try:
            dest = self[p2]
        except:
            pass
        del self[p1]
        self[p2] = piece

    def complete_move(self, piece, dest, p1, p2):
        enemy = ('white' if piece.color == 'black' else 'black')
        if piece.color == 'black':
            self.fullmove_number += 1
        self.halfmove_clock += 1
        self.player_turn = enemy
        abbr = piece.shortname
        if abbr == 'P':
            abbr = ''
            self.halfmove_clock = 0
        if dest is None:
            movetext = abbr + p2.lower()
        else:
            movetext = abbr + 'x' + p2.lower()
            self.halfmove_clock = 0
        self.history.append(movetext)

    def all_moves_available(self, color):

        result = []
        for coord in self.keys():
            if (self[coord] is not None) and self[coord].color == color:
                moves = self[coord].moves_available(coord)
                if moves: result += moves
        return result

    def occupied(self, color):
        result = []
        for coord in iter(self.keys()):
            if self[coord].color == color:
                result.append(coord)
        return result
        
    def num_notation(self, coord):
        return int(coord[1]) - 1, self.y_axis.index(coord[0])

    def position_of_king(self, color):
        for pos in self.keys():
            if isinstance(self[pos], cm.King) and self[pos].color == color:
                return pos

    def king_in_check(self, color):
        kingpos = self.position_of_king(color)
        opponent = ('black' if color == 'white' else 'white')
        for pieces in self.items():
            if kingpos in self.all_moves_available(opponent):
                return True
            else:
                return False


    # def show(self, pat):
    #     self.clear()
    #     def expand(match):
    #         return ' ' * int(match.group(0))

    #     for x, row in enumerate(pat[0].split('/')):
    #         for y, letter in enumerate(row):
    #             if letter == ' ': continue
    #             coord = self.alpha_notation((7 - x, y))
    #             self[coord] = pieces.create_piece(letter)
    #             self[coord].place(self)
    #     if pat[1] == 'w':
    #         self.player_turn = 'white'
    #     else:
    #         self.player_turn = 'black'
    #     self.halfmove_clock = int(pat[2])
    #     self.fullmove_number = int(pat[3])


class ChessError(Exception): pass


class Check(ChessError): pass


class InvalidMove(ChessError): pass


class CheckMate(ChessError): pass


class Draw(ChessError): pass


class NotYourTurn(ChessError): pass


class InvalidCoord(ChessError): pass
