from Pieces import *
from Game import *


class Board:
    def __init__(self, game):
        # key : coords -> val : pieces
        self.pieces = dict()
        self.game = game

    def set_piece(self, coordinates: tuple, piece: Piece):
        piece.coords = coordinates
        self.pieces[coordinates] = piece

    def remove_piece(self, coordinates: tuple):
        self.pieces.pop(coordinates)

    def move_piece(self, start_pos: tuple, finish_pos: tuple):
        piece = self.pieces[start_pos]
        self.remove_piece(start_pos)
        self.set_piece(finish_pos, piece)

    def is_cell_empty(self, coordinates: tuple):
        return not (coordinates in self.pieces)

    def get_piece(self, coordinates: tuple):
        return self.pieces[coordinates]

    @classmethod
    def is_cell_white(cls, coordinates: tuple):
        return ((coordinates[0] + coordinates[1]) % 2) == 1

    def find_coords_figure_by_type_and_color(self, type: str, color: str):
        for coords, piece in self.pieces.items():
            if (piece.type_of_piece == type and piece.color == color):
                return coords
        return (-1, -1)

    def get_opponent_attacked_cells(self, color: str):
        if (color == "BLACK"):
            opponent_color = "WHITE"
        else:
            opponent_color = "BLACK"
        opponent_cells = set()
        for piece in self.pieces.values():
            if piece.color == opponent_color and piece.type_of_piece != "King":
                for cells in piece.get_possible_cells_to_attack(self):
                    opponent_cells.add(cells)
        return opponent_cells

class BoardFactoryAndTransormatorToFEN:
    const_digits = '0123456789'
    black_notation = 'pnbrqk'
    white_notation = 'PNBRQK'
    pieces_dict = {
        "p": Pawn,
        "n": Knight,
        "b": Bishop,
        "r": Rook,
        "q": Queen,
        "k": King,
    }

    def build_board_by_FEN(self, game, FEN_notation: str) -> Board:
        # rnbqk2r/pppp1ppp/4p2n/1BbN1Q2/3PP3/5P2/PPP3PP/R1B1K1NR w KQkq - 0 1
        new_board = Board(game)
        get_board_notation = FEN_notation.split()[0].split('/')
        for rank in range(8, 0, -1):
            row = get_board_notation[8 - rank]
            file = 1
            for symb in row:
                if (symb in self.const_digits):
                    file += int(symb)
                    continue
                if (symb in self.white_notation):
                    new_board.set_piece((file, rank), self.pieces_dict[symb.lower()](Colors.colors[0], (file, rank)))
                else:
                    new_board.set_piece((file, rank), self.pieces_dict[symb](Colors.colors[1], (file, rank)))
                file += 1
        return new_board
