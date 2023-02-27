from board import Board, Position
from move import MoveCategory
from pieces import Colour, Piece, PieceType


def get_moves(board: Board, piece: Piece, move_type: MoveCategory) -> list[Position]:
    moves: list[Position] = []
    for move_func in piece.move_type[move_type.value]:
        print(move_func)
        valid_moves = move_func.get_valid_moves(board, piece.x, piece.y)
        print(valid_moves)
        moves.extend(valid_moves)
    return moves


def king_is_in_check(board: Board, colour: Colour) -> bool:
    king_position = board.find_king(colour)

    all_moves: list[Position] = []
    for piece in board.pieces.values():
        if piece.colour != colour and piece.type != PieceType.EMPTY:
            possible_moves = get_moves(board, piece, MoveCategory.CAPTURE)
            all_moves.extend(possible_moves)

    return king_position in all_moves
