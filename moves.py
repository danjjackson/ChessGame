from typing import Callable, Protocol

from exceptions import IllegalMoveError, NotationError, OutOfBoundsError
from pieces import PieceType
from square import Square
from utils import Colour, MoveCategory


class Board(Protocol):
    def get_square(self, file: str, rank: str) -> Square:
        """Returns the piece at position (x, y)."""
        return Square()


def get_vertical_neighbour(board: Board, square: Square, orientation: Colour) -> Square:
    try:
        square = (
            board.get_square(square.file, chr(ord(square.rank) + 1))
            if orientation == Colour.WHITE
            else board.get_square(square.file, chr(ord(square.rank) - 1))
        )
    except OutOfBoundsError as e:
        raise e
    return square


def get_horizontal_neighbour(
    board: Board, square: Square, orientation: Colour
) -> Square:
    try:
        square = (
            board.get_square(chr(ord(square.file) + 1), square.rank)
            if orientation == Colour.WHITE
            else board.get_square(chr(ord(square.file) - 1), square.rank)
        )
    except KeyError:
        raise KeyError
    return square


def get_positive_diagonal_neighbour(
    board: Board, square: Square, orientation: Colour
) -> Square:
    try:
        square = (
            board.get_square(chr(ord(square.file) + 1), chr(ord(square.rank) + 1))
            if orientation == Colour.WHITE
            else board.get_square(chr(ord(square.file) - 1), chr(ord(square.rank) - 1))
        )
    except OutOfBoundsError as e:
        raise e
    return square


def get_negative_diagonal_neighbour(
    board: Board, square: Square, orientation: Colour
) -> Square:
    try:
        square = (
            board.get_square(chr(ord(square.file) - 1), chr(ord(square.rank) + 1))
            if orientation == Colour.WHITE
            else board.get_square(chr(ord(square.file) + 1), chr(ord(square.rank) - 1))
        )
    except OutOfBoundsError as e:
        raise e
    return square


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


def is_valid_knight_move(
    board: Board, source: Square, target: Square, move_category: MoveCategory
) -> bool:
    coordinates = [
        (chr(ord(source.file) + 1), chr(ord(source.rank) + 2)),
        (chr(ord(source.file) + 1), chr(ord(source.rank) - 2)),
        (chr(ord(source.file) - 1), chr(ord(source.rank) + 2)),
        (chr(ord(source.file) - 1), chr(ord(source.rank) - 2)),
        (chr(ord(source.file) + 2), chr(ord(source.rank) + 1)),
        (chr(ord(source.file) + 2), chr(ord(source.rank) - 1)),
        (chr(ord(source.file) - 2), chr(ord(source.rank) + 1)),
        (chr(ord(source.file) - 2), chr(ord(source.rank) - 1)),
    ]

    for coordinate in coordinates:
        try:
            square = board.get_square(*coordinate)
            if square == target:
                if square.piece.colour == source.piece.colour:
                    raise IllegalMoveError(
                        "That square is already occupied by one of your pieces!"
                    )
                if move_category == MoveCategory.REGULAR:
                    if square.is_empty:
                        return True
                    else:
                        raise NotationError(
                            "The square is occupied by your opponents piece. Do you want to capture it?"
                        )
                if move_category == MoveCategory.CAPTURE:
                    if square.is_empty:
                        raise NotationError(
                            "There isn't a piece on that square to capture!"
                        )
                    else:
                        return True
        except OutOfBoundsError:
            continue

    return False


def is_short_castle_valid(board: Board, source: Square) -> bool:
    if source.piece.has_moved:
        return False

    bishop_square = board.get_square(chr(ord(source.file) + 1), source.rank)
    knight_square = board.get_square(chr(ord(source.file) + 2), source.rank)
    rook_square = board.get_square(chr(ord(source.file) + 3), source.rank)

    if (
        not rook_square.piece.has_moved
        and bishop_square.is_empty
        and knight_square.is_empty
    ):
        return True

    else:
        return False


def is_long_castle_valid(board: Board, source: Square) -> bool:
    if source.piece.has_moved:
        return False

    queen_square = board.get_square(chr(ord(source.file) - 1), source.rank)
    bishop_square = board.get_square(chr(ord(source.file) - 2), source.rank)
    knight_square = board.get_square(chr(ord(source.file) - 3), source.rank)
    rook_square = board.get_square(chr(ord(source.file) - 4), source.rank)

    if (
        not rook_square.piece.has_moved
        and queen_square.is_empty
        and bishop_square.is_empty
        and knight_square.is_empty
    ):
        return True

    else:
        return False
