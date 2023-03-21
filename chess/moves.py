from typing import Callable, Protocol

from chess.exceptions import IllegalMoveError, OutOfBoundsError
from chess.pieces import PieceType
from chess.square import Square
from chess.utils import Colour, MoveCategory


class Board(Protocol):
    def get_square(self, file: int, rank: int) -> Square:
        """Returns the piece at position (x, y)."""
        return Square(file, rank)


def get_vertical_neighbour(board: Board, square: Square, direction: Colour) -> Square:
    return (
        board.get_square(square.file, square.rank - 1)
        if direction == Colour.WHITE
        else board.get_square(square.file, square.rank + 1)
    )


def get_horizontal_neighbour(board: Board, square: Square, direction: Colour) -> Square:
    return (
        board.get_square(square.file - 1, square.rank)
        if direction == Colour.WHITE
        else board.get_square(square.file + 1, square.rank)
    )


def get_positive_diagonal_neighbour(
    board: Board, square: Square, direction: Colour
) -> Square:
    return (
        board.get_square(square.file - 1, square.rank - 1)
        if direction == Colour.WHITE
        else board.get_square(square.file + 1, square.rank + 1)
    )


def get_negative_diagonal_neighbour(
    board: Board, square: Square, orientation: Colour
) -> Square:
    return (
        board.get_square(square.file + 1, square.rank - 1)
        if orientation == Colour.WHITE
        else board.get_square(square.file - 1, square.rank + 1)
    )


def get_knight_squares(board: Board, square: Square) -> list[Square]:
    coordinates = [
        (square.file + 1, square.rank + 2),
        (square.file + 1, square.rank - 2),
        (square.file - 1, square.rank + 2),
        (square.file - 1, square.rank - 2),
        (square.file + 2, square.rank + 1),
        (square.file + 2, square.rank - 1),
        (square.file - 2, square.rank + 1),
        (square.file - 2, square.rank - 1),
    ]

    squares = []
    for coordinate in coordinates:
        try:
            square = board.get_square(*coordinate)
            squares.append(square)
        except OutOfBoundsError:
            continue

    return squares


def is_short_castle_valid(board: Board, source: Square) -> bool:
    if source.piece.has_moved:
        raise IllegalMoveError(
            "Your king has already moved - you cannot castle anymore!"
        )

    bishop_square = board.get_square(source.file + 1, source.rank)
    knight_square = board.get_square(source.file + 2, source.rank)
    rook_square = board.get_square(source.file + 3, source.rank)

    if rook_square.is_empty or rook_square.piece.has_moved:
        raise IllegalMoveError("You've moved your kingside rook!")

    if not bishop_square.is_empty or not knight_square.is_empty:
        raise IllegalMoveError(
            "You need to move your knight and bishop out of the way before you can castle!"
        )

    return True


def is_long_castle_valid(board: Board, source: Square) -> bool:
    if source.piece.has_moved:
        raise IllegalMoveError(
            "Your king has already moved - you cannot castle anymore!"
        )

    queen_square = board.get_square(source.file - 1, source.rank)
    bishop_square = board.get_square(source.file - 2, source.rank)
    knight_square = board.get_square(source.file - 3, source.rank)
    rook_square = board.get_square(source.file - 4, source.rank)

    if rook_square.is_empty or rook_square.piece.has_moved:
        raise IllegalMoveError("You've moved your queenside rook!")

    if (
        not bishop_square.is_empty
        or not knight_square.is_empty
        or not queen_square.is_empty
    ):
        raise IllegalMoveError(
            "You need to move your queen, knight and bishop out of the way before you can castle!"
        )

    return True


NeighbourCalculator = Callable[[Board, Square, Colour], Square]


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
            get_positive_diagonal_neighbour,
            get_negative_diagonal_neighbour,
            get_vertical_neighbour,
            get_horizontal_neighbour,
        ],
        MoveCategory.CAPTURE: [
            get_positive_diagonal_neighbour,
            get_negative_diagonal_neighbour,
            get_vertical_neighbour,
            get_horizontal_neighbour,
        ],
    },
    PieceType.KING: {
        MoveCategory.REGULAR: [
            get_positive_diagonal_neighbour,
            get_negative_diagonal_neighbour,
            get_vertical_neighbour,
            get_horizontal_neighbour,
        ],
        MoveCategory.CAPTURE: [
            get_positive_diagonal_neighbour,
            get_negative_diagonal_neighbour,
            get_vertical_neighbour,
            get_horizontal_neighbour,
        ],
    },
}
# MOVEMENT_MAP: dict[PieceType, dict[MoveCategory, list[NeighbourCalculator]]] = {
#     PieceType.PAWN: {
#         MoveCategory.REGULAR: [get_rank],
#         MoveCategory.CAPTURE: [get_forwards_diagonals],
#     },
#     PieceType.ROOK: {
#         MoveCategory.REGULAR: [get_rank, get_file],
#         MoveCategory.CAPTURE: [get_rank, get_file],
#     },
#     PieceType.BISHOP: {
#         MoveCategory.REGULAR: [
#             get_forwards_diagonals,
#             get_backwards_diagonals,
#         ],
#         MoveCategory.CAPTURE: [
#             get_forwards_diagonals,
#             get_backwards_diagonals,
#         ],
#     },
#     PieceType.QUEEN: {
#         MoveCategory.REGULAR: [
#             get_file,
#             get_rank,
#             get_forwards_diagonals,
#             get_backwards_diagonals,
#         ],
#         MoveCategory.CAPTURE: [
#             get_file,
#             get_rank,
#             get_forwards_diagonals,
#             get_backwards_diagonals,
#         ],
#     },
#     PieceType.KING: {
#         MoveCategory.REGULAR: [
#             get_file,
#             get_rank,
#             get_forwards_diagonals,
#             get_backwards_diagonals,
#         ],
#         MoveCategory.CAPTURE: [
#             get_file,
#             get_rank,
#             get_forwards_diagonals,
#             get_backwards_diagonals,
#         ],
#     },
# }
