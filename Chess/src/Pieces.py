from abc import ABC, abstractmethod
from src.MovePieces import *


# import MovesPieces


class Colors:
    colors = {
        0: 'WHITE',
        1: 'BLACK'
    }
    this_color = colors[0]

    def __init__(self, color):
        self.this_color = self.colors[color]


class File:
    Files = {
        1: 'A',
        2: 'B',
        3: 'C',
        4: 'D',
        5: 'E',
        6: 'F',
        7: 'G',
        8: 'H',
    }

    def get_values(self):
        return self.Files


class Piece(ABC):
    type_of_piece = ''

    def __init__(self, color, coords: tuple):
        self.color = color
        self.coords = coords

    @abstractmethod
    def get_possible_moves(self):
        pass

    @abstractmethod
    def is_possible_to_move(self, potential_moves, board):
        if (1 > potential_moves[0]) or (potential_moves[0] > 8) or (1 > potential_moves[1]) or (potential_moves[1] > 8):
            return False
        if (board.is_cell_empty(potential_moves) or board.get_piece(potential_moves).color !=
                self.color):
            return True
        return False

    def get_possible_cells_to_attack(self, board):
        result_set = set()
        for move in self.get_possible_moves():
            potential_moves = (self.coords[0] + move[0], self.coords[1] + move[1])
            if self.is_possible_to_move(potential_moves, board):
                result_set.add(potential_moves)
        return result_set

    def get_possible_cells_to_move(self, board):
        result_set = set()
        for move in self.get_possible_moves():
            potential_moves = (self.coords[0] + move[0], self.coords[1] + move[1])
            if not self.is_possible_to_move(potential_moves, board):
                continue
            if self.type_of_piece != "King":
                copy = ""
                if not (board.is_cell_empty(potential_moves)):
                    copy = board.get_piece(potential_moves)
                copy_coords = self.coords
                board.move_piece(self.coords, potential_moves)
                king_coords = board.find_coords_figure_by_type_and_color("King", self.color)
                if not (king_coords in board.get_opponent_attacked_cells(self.color)):
                    result_set.add(potential_moves)
                board.move_piece(potential_moves, copy_coords)
                if (copy != ""):
                    board.set_piece(potential_moves, copy)
            else:
                result_set.add(potential_moves)
        return result_set


class Pawn(Piece):
    type_of_piece = "Pawn"

    def __init__(self, color, coords: tuple):
        super().__init__(color, coords)

    def is_possible_to_move(self, potential_move, board):
        return super().is_possible_to_move(potential_move, board) and IsPawnCorrect(board, self.coords, potential_move)

    def get_possible_moves(self):
        arr_moves = []
        if (self.color == "WHITE"):
            if (self.coords[1] == 2):
                arr_moves.append((0, 2))
            arr_moves.append((0, 1))
            arr_moves.append((1, 1))
            arr_moves.append((-1, 1))
        else:
            if (self.coords[1] == 7):
                arr_moves.append((0, -2))
            arr_moves.append((0, -1))
            arr_moves.append((1, -1))
            arr_moves.append((-1, -1))
        return arr_moves

class Knight(Piece):
    type_of_piece = "Knight"

    def __init__(self, color, coords: tuple):
        super().__init__(color, coords)

    def is_possible_to_move(self, move, board):
        return super().is_possible_to_move(move, board)

    def get_possible_moves(self):
        return [
            (-2, 1),
            (-1, 2),

            (-2, -1),
            (-1, -2),

            (1, 2),
            (2, 1),

            (2, -1),
            (1, -2)
        ]


class Bishop(Piece):
    type_of_piece = "Bishop"

    def __init__(self, color, coords: tuple):
        super().__init__(color, coords)

    def is_possible_to_move(self, potential_move, board):
        result = super().is_possible_to_move(potential_move, board)
        # return result
        return result and GetDiagonalAndStrictMoves(board, self.coords, potential_move)

    def get_possible_moves(self):
        result_list = []
        for i in range(-8, 9):
            for j in range(-8, 9):
                if (i == j) or (i == -j):
                    result_list.append((i, j))

        return result_list


class Rook(Piece):
    type_of_piece = "Rook"

    def __init__(self, color, coords: tuple):
        super().__init__(color, coords)

    def is_possible_to_move(self, potential_move, board):
        result = super().is_possible_to_move(potential_move, board)
        return result and GetDiagonalAndStrictMoves(board, self.coords, potential_move)

    def get_possible_moves(self):
        result_list = []
        for i in range(-8, 9):
            result_list.append((i, 0))
            result_list.append((0, i))
        return result_list


class Queen(Piece):
    type_of_piece = "Queen"

    def __init__(self, color, coords: tuple):
        super().__init__(color, coords)

    def is_possible_to_move(self, potential_move, board):
        return super().is_possible_to_move(potential_move, board) and GetDiagonalAndStrictMoves(board, self.coords,
                                                                                                potential_move)

    def get_possible_moves(self):
        result_list = []
        for i in range(-8, 9):
            result_list.append((i, 0))
            result_list.append((0, i))
        for i in range(-8, 9):
            for j in range(-8, 9):
                if (i == j) or (i == -j):
                    result_list.append((i, j))
        return result_list


class King(Piece):
    type_of_piece = "King"

    def __init__(self, color, coords: tuple):
        super().__init__(color, coords)

    def is_possible_to_move(self, potential_move, board):
        return super().is_possible_to_move(potential_move, board) and CheckKingMoves(board, self.color, self.coords,
                                                                                     potential_move)

    def get_possible_moves(self):
        result_list = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == j == 0):
                    result_list.append((i, j))
        return result_list
