import Pieces


# this file contains all method for checking moves
def GetDiagonalAndStrictMoves(board, start_cell, finish_cell):
    if (start_cell[0] - finish_cell[0]) != 0 and (start_cell[1] - finish_cell[1]) != 0:
        direction_of_ray = (- (start_cell[0] - finish_cell[0]) // abs(start_cell[0] - finish_cell[0]),
                            - (start_cell[1] - finish_cell[1]) // abs(
                                start_cell[1] - finish_cell[1]))
    elif (start_cell[0] - finish_cell[0]) == 0:
        direction_of_ray = (0, -(start_cell[1] - finish_cell[1]) // abs(
            start_cell[1] - finish_cell[1]))
    else:
        direction_of_ray = (- (start_cell[0] - finish_cell[0]) // abs(
            start_cell[0] - finish_cell[0]), 0)
    cpy_cell = list(start_cell)
    cpy_cell[0] += direction_of_ray[0]
    cpy_cell[1] += direction_of_ray[1]
    while (cpy_cell[0] != finish_cell[0]) or (cpy_cell[1] != finish_cell[1]):
        if not board.is_cell_empty((cpy_cell[0], cpy_cell[1])):
            return False
        cpy_cell[0] += direction_of_ray[0]
        cpy_cell[1] += direction_of_ray[1]
    return True


def IsPawnCorrect(board, start_cell: tuple, finish_cell: tuple) -> bool:
    direction_of_ray = (start_cell[0] - finish_cell[0], (start_cell[1] - finish_cell[1]))
    if (direction_of_ray[0] * direction_of_ray[1] != 0):
        return (not board.is_cell_empty(finish_cell)) and board.get_piece(finish_cell).color != board.get_piece(
            start_cell).color
    else:
        return board.is_cell_empty(finish_cell) and GetDiagonalAndStrictMoves(board, start_cell, finish_cell)


def CheckKingMoves(board, color: str, start_cell: tuple, finish_cell: tuple) -> bool:
    copy = ''
    if not (board.is_cell_empty(finish_cell)):
        copy = board.get_piece(finish_cell)
    board.move_piece(start_cell, finish_cell)
    result = not (finish_cell in board.get_opponent_attacked_cells(color))
    board.move_piece(finish_cell, start_cell)
    if (copy != ''):
        board.set_piece(finish_cell, copy)
    return result
