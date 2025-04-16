from src.Board import *
from src.coder import Coder


class InputedCoords:

    @classmethod
    def is_format_correct(cls, inpt: str):
        dig = "12345678"
        alph = "abcdefgh"
        if (len(inpt) != 2):
            return False
        if (not (inpt[0].lower() in alph)) or (not (inpt[1] in dig)):
            return False
        return True

    @classmethod
    def transform(cls, coords: str):
        alph = "abcdefgh"
        return (alph.index(coords[0].lower()) + 1, int(coords[1]))

    @classmethod
    def input_coords(cls, inp):
        # self.game.return_data("enter coords divided by space for ex (c6 c8) + \n")
        coords = inp.split()
        coords = coords[:2]
        if not ((InputedCoords.is_format_correct(coords[0])) and (InputedCoords.is_format_correct(coords[1]))):
            return (-1, -1)
        coords_from = InputedCoords.transform(coords[0])
        coords_too = InputedCoords.transform(coords[1])
        return [coords_from, coords_too]

    @classmethod
    def is_move_correct(cls, is_white, candidate_move, board):

        if (board.is_cell_empty(candidate_move[0])) or (
                board.get_piece(candidate_move[0]).color != ["BLACK", "WHITE"][is_white]):
            return False

        coords_from, coords_to = candidate_move
        piece = board.get_piece(coords_from)

        possible_moves = piece.get_possible_cells_to_move(board)
        return coords_to in possible_moves


class Game:
    def __init__(self, server):
        self.board = BoardFactoryAndTransormatorToFEN().build_board_by_FEN(self,
                                                                           "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.server = server
        self.cnt_turns = 0
        self.input_coord = InputedCoords
        self.game_status = 0

    def return_data(self, data, code, players="all"):
        self.server.receive_from_game(data, code, players)

    def cant_move(self, color):
        for coord, piece in self.board.pieces.items():
            if piece.color == color:
                if len(piece.get_possible_cells_to_move(self.board)) != 0:
                    return False
        return True

    def input_data(self, data):
        coord = self.input_coord.input_coords(data)
        color = "WHITE" if self.cnt_turns % 2 == 0 else "BLACK"
        if (coord[0] != -1):
            if self.input_coord.is_move_correct(self.cnt_turns % 2 == 0, coord, self.board):
                self.board.move_piece(coord[0], coord[1])
                if self.cant_move(color) or self.cnt_turns >= 2:
                    self.return_data(f"{Coder.encode(self.board)}|ENDGAME {color} lost\n", "end", "first")
                    self.return_data(f"{Coder.encode(self.board)}|ENDGAME {color} lost\n", "end", "second")
                else:
                    if (color == "WHITE"):
                        self.return_data(f"{Coder.encode(self.board)}|Enter move, sempai!", "active", "first")
                        self.return_data(f"{Coder.encode(self.board)}|", "active", "second")
                        self.cnt_turns += 1
                    else:
                        self.return_data(f"{Coder.encode(self.board)}|Enter move, sempai!", "active", "second")
                        self.return_data(f"{Coder.encode(self.board)}|", "active", "first")
                        self.cnt_turns += 1
            else:
                if (color == "WHITE"):
                    self.return_data(f"{Coder.encode(self.board)}|Invalid format entered try one more time + \n",
                                     "active",
                                     "second")
                else:
                    self.return_data(f"{Coder.encode(self.board)}|Another player submitted cringe \n", "active",
                                     "first")
        else:
            if (color == "WHITE"):
                self.return_data(f"{Coder.encode(self.board)}|Invalid format entered try one more time + \n", "active",
                                 "second")
            else:
                self.return_data(f"{Coder.encode(self.board)}|Another player submitted cringe \n", "active",
                                 "first")
