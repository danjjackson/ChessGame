from enum import Enum, StrEnum, auto

# from board import Board
# from pieces import Piece, PieceType
# from square import Square

notation_map = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}


class MoveCategory(StrEnum):
    REGULAR = auto()
    CAPTURE = auto()
    SHORT_CASTLE = auto()
    LONG_CASTLE = auto()


class Colour(Enum):
    BLANK = -1
    WHITE = 0
    BLACK = 1


# def get_moves(board: Board, square: Square, move_type: MoveCategory) -> list[Position]:
#     moves: list[Position] = []
#     for move_func in square.piece.move_type[move_type.value]:
#         print(move_func)
#         valid_moves = move_func.get_valid_moves(board, square.file, square.rank)
#         print(valid_moves)
#         moves.extend(valid_moves)
#     return moves


# def is_reachable(
#     board: Board, source: Square, destination: Square, move_category: MoveCategory
# ) -> bool:
#     reachable = False
#     for movement_class in source.piece.move_type[move_category]:
#         if movement_class.is_reachable(board, source, destination):
#             reachable = True

#     return reachable
