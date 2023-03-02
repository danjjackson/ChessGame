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
    return (
        board.get_square(square.file, chr(ord(square.rank) + 1))
        if orientation == Colour.WHITE
        else board.get_square(square.file, chr(ord(square.rank) - 1))
    )


def get_horizontal_neighbour(
    board: Board, square: Square, orientation: Colour
) -> Square:
    return (
        board.get_square(chr(ord(square.file) + 1), square.rank)
        if orientation == Colour.WHITE
        else board.get_square(chr(ord(square.file) - 1), square.rank)
    )


def get_positive_diagonal_neighbour(
    board: Board, square: Square, orientation: Colour
) -> Square:
    return (
        board.get_square(chr(ord(square.file) + 1), chr(ord(square.rank) + 1))
        if orientation == Colour.WHITE
        else board.get_square(chr(ord(square.file) - 1), chr(ord(square.rank) - 1))
    )


def get_negative_diagonal_neighbour(
    board: Board, square: Square, orientation: Colour
) -> Square:
    return (
        board.get_square(chr(ord(square.file) - 1), chr(ord(square.rank) + 1))
        if orientation == Colour.WHITE
        else board.get_square(chr(ord(square.file) + 1), chr(ord(square.rank) - 1))
    )


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
        raise IllegalMoveError(
            "Your king has already moved - you cannot castle anymore!"
        )

    bishop_square = board.get_square(chr(ord(source.file) + 1), source.rank)
    knight_square = board.get_square(chr(ord(source.file) + 2), source.rank)
    rook_square = board.get_square(chr(ord(source.file) + 3), source.rank)

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

    queen_square = board.get_square(chr(ord(source.file) - 1), source.rank)
    bishop_square = board.get_square(chr(ord(source.file) - 2), source.rank)
    knight_square = board.get_square(chr(ord(source.file) - 3), source.rank)
    rook_square = board.get_square(chr(ord(source.file) - 4), source.rank)

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
