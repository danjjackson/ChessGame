from dataclasses import dataclass
from typing import Callable, Protocol

from pieces import PieceType
from square import Square
from utils import Colour, MoveCategory


class Board(Protocol):
    def get_square(self, file: str, rank: str) -> Square | None:
        """Returns the piece at position (x, y)."""
        return None


def get_vertical_neighbour(
    board: Board, square: Square, orientation: Colour
) -> Square | None:
    return (
        board.get_square(square.file, chr(ord(square.rank) + 1))
        if orientation == Colour.WHITE
        else board.get_square(square.file, chr(ord(square.rank) - 1))
    )


def get_horizontal_neighbour(
    board: Board, square: Square, orientation: Colour
) -> Square | None:
    return (
        board.get_square(chr(ord(square.file) + 1), square.rank)
        if orientation == Colour.WHITE
        else board.get_square(chr(ord(square.file) - 1), square.rank)
    )


def get_positive_diagonal_neighbour(
    board: Board, square: Square, orientation: Colour
) -> Square | None:
    return (
        board.get_square(chr(ord(square.file) + 1), chr(ord(square.rank) + 1))
        if orientation == Colour.WHITE
        else board.get_square(chr(ord(square.file) - 1), chr(ord(square.rank) - 1))
    )


def get_negative_diagonal_neighbour(
    board: Board, square: Square, orientation: Colour
) -> Square | None:
    return (
        board.get_square(chr(ord(square.file) - 1), chr(ord(square.rank) + 1))
        if orientation == Colour.WHITE
        else board.get_square(chr(ord(square.file) + 1), chr(ord(square.rank) - 1))
    )


NeighbourCalculator = Callable[[Board, Square, Colour], Square | None]
MOVEMENT_MAP: dict[PieceType, dict[MoveCategory, list[NeighbourCalculator]]] = {
    PieceType.PAWN: {
        MoveCategory.REGULAR: [get_vertical_neighbour],
        MoveCategory.CAPTURE: [
            get_positive_diagonal_neighbour,
            get_negative_diagonal_neighbour,
        ],
    },
    PieceType.ROOK: {
        MoveCategory.REGULAR: [get_vertical_neighbour, get_horizontal_neighbour],
        MoveCategory.CAPTURE: [get_vertical_neighbour, get_horizontal_neighbour],
    },
    PieceType.BISHOP: {
        MoveCategory.REGULAR: [
            get_positive_diagonal_neighbour,
            get_negative_diagonal_neighbour,
        ],
        MoveCategory.CAPTURE: [
            get_positive_diagonal_neighbour,
            get_negative_diagonal_neighbour,
        ],
    },
    PieceType.QUEEN: {
        MoveCategory.REGULAR: [
            get_vertical_neighbour,
            get_horizontal_neighbour,
            get_positive_diagonal_neighbour,
            get_negative_diagonal_neighbour,
        ],
        MoveCategory.CAPTURE: [
            get_vertical_neighbour,
            get_horizontal_neighbour,
            get_positive_diagonal_neighbour,
            get_negative_diagonal_neighbour,
        ],
    },
    PieceType.KING: {
        MoveCategory.REGULAR: [
            get_vertical_neighbour,
            get_horizontal_neighbour,
            get_positive_diagonal_neighbour,
            get_negative_diagonal_neighbour,
        ],
        MoveCategory.CAPTURE: [
            get_vertical_neighbour,
            get_horizontal_neighbour,
            get_positive_diagonal_neighbour,
            get_negative_diagonal_neighbour,
        ],
    },
}


def is_valid_knight_move(board: Board, source: Square, target: Square) -> bool:
    squares = [
        board.get_square(chr(ord(source.file) + 1), chr(ord(source.rank) + 2)),
        board.get_square(chr(ord(source.file) + 1), chr(ord(source.rank) - 2)),
        board.get_square(chr(ord(source.file) - 1), chr(ord(source.rank) + 2)),
        board.get_square(chr(ord(source.file) - 1), chr(ord(source.rank) - 2)),
        board.get_square(chr(ord(source.file) + 2), chr(ord(source.rank) + 1)),
        board.get_square(chr(ord(source.file) + 2), chr(ord(source.rank) - 1)),
        board.get_square(chr(ord(source.file) - 2), chr(ord(source.rank) + 1)),
        board.get_square(chr(ord(source.file) - 2), chr(ord(source.rank) - 1)),
    ]

    valid_squares: list[Square] = []

    for square in squares:
        if square is not None:
            if square.is_empty or square.piece.colour != source.piece.colour:
                valid_squares.append(square)

    return target in valid_squares


def is_short_castle_valid(board: Board, source: Square) -> bool:
    bishop_square = board.get_square(chr(ord(source.file) + 1), source.rank)
    knight_square = board.get_square(chr(ord(source.file) + 2), source.rank)
    rook_square = board.get_square(chr(ord(source.file) + 3), source.rank)

    print(rook_square)

    if (
        not source.piece.has_moved
        and not rook_square.piece.has_moved
        and bishop_square.is_empty
        and knight_square.is_empty
    ):
        return True

    else:
        return False


# class LongCastle(MoveType):
#     def get_valid_moves(self, board: Board, x: int, y: int) -> list[Position]:
#         valid_moves = []
#         if (
#             not board.piece(x, y).has_moved
#             and not board.piece(x, y - 4).has_moved
#             and board.is_empty(x, y - 1)
#             and board.is_empty(x, y - 2)
#             and board.is_empty(x, y - 2)
#         ):
#             valid_moves.append((x, y - 2))

#         return valid_moves
