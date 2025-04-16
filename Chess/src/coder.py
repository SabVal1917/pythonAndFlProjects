class Coder:
    # ansi colors
    @classmethod
    def encode(cls, board):
        notatinon_dict = {
            "Pawn": "p",
            "Knight": "n",
            "Bishop": "b",
            "Rook": "r",
            "Queen": "q",
            "King": "k"
        }
        notation = ""
        for rank in range(8, 0, -1):
            row = ""
            counter_empty_cells = 0
            for file in range(1, 9):
                if board.is_cell_empty((file, rank)):
                    counter_empty_cells += 1
                else:
                    if counter_empty_cells != 0:
                        row += str(counter_empty_cells)
                    counter_empty_cells = 0
                    new_piece = board.get_piece((file, rank))
                    if new_piece.color == "WHITE":
                        row += notatinon_dict[new_piece.type_of_piece].upper()
                    else:
                        row += notatinon_dict[new_piece.type_of_piece]
            else:
                if counter_empty_cells != 0:
                    row += str(counter_empty_cells)
                notation += row + '/'
        return notation

    @classmethod
    def decode(cls, coded_FEN):
        if not ("/" in coded_FEN):
            return coded_FEN
        res = ""
        get_board_notation = coded_FEN.split()[0].split('/')

        const_digits = '0123456789'
        # black_notation = 'pnbrqk'
        white_notation = 'PNBRQK'
        ANSI_RESET = "\u001B[0m"
        ANSI_WHITE_PIECE_COLOR = "\u001B[97m"
        ANSI_BLACK_PIECE_COLOR = "\u001B[30m"
        ANSI_WHITE_SQUARE_BACKGROUND = "\u001B[47m"
        ANSI_BLACK_SQUARE_BACKGROUND = "\u001B[0;100m"

        def colorize_sprite(sprite: str, color: str, is_cell_white: bool):
            result = sprite
            if ("WHITE" == color):
                result = ANSI_WHITE_PIECE_COLOR + result
            else:
                result = ANSI_BLACK_PIECE_COLOR + result
            if (is_cell_white):
                result = ANSI_WHITE_SQUARE_BACKGROUND + result
            else:
                result = ANSI_BLACK_SQUARE_BACKGROUND + result
            return result

        def color_empty_cell(coords: tuple):
            return colorize_sprite("   ", "WHITE", is_cell_white(coords))

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

        get_piece_sprite = {
            "p": "♟︎",
            "n": "♞",
            "b": "♝",
            "r": "♜",
            "q": "♛",
            "k": "♚"
        }

        def is_cell_white(coords: tuple):
            return (coords[0] + coords[1]) % 2 != 0

        def color_piece_cell(piece: str, color: str, coords: tuple):
            return colorize_sprite(" " + get_piece_sprite[piece] + " ", color,
                                   is_cell_white(coords))

        for rank in range(8, 0, -1):
            print(res)
            row = get_board_notation[8 - rank]
            file = 1
            for symb in row:
                if (symb in const_digits):
                    for j in range(file, file + int(symb)):
                        res += color_empty_cell((j, rank))
                    file += int(symb)
                    continue
                if (symb in white_notation):
                    res += color_piece_cell(symb.lower(), "WHITE", (file, rank))
                else:
                    res += color_piece_cell(symb.lower(), "BLACK", (file, rank))
                file += 1
            res += ANSI_RESET
            res += ' ' + str(rank) + '\n'
        for file in range(1, 9):
            res += " " + Files[file] + " "
        return res + '\n'
