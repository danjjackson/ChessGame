from typing import Callable, Literal, Protocol

from chess.exceptions import IllegalMoveError, OutOfBoundsError
from chess.pieces import PieceType
from chess.square import Square
from chess.utils import Colour, MoveCategory


class Board(Protocol):
    def get_square(self, file: int, rank: int) -> Square:
        raise NotImplementedError


def get_DS_neighbour(board: Board, square: Square) -> Square:
    return board.get_square(square.file, square.rank + 1)


def get_US_neighbour(board: Board, square: Square) -> Square:
    return board.get_square(square.file, square.rank - 1)


def get_SL_neighbour(board: Board, square: Square) -> Square:
    return board.get_square(square.file - 1, square.rank)


def get_SR_neighbour(board: Board, square: Square) -> Square:
    return board.get_square(square.file + 1, square.rank)


def get_DSR_neighbour(board: Board, square: Square) -> Square:
    return board.get_square(square.file + 1, square.rank + 1)


def get_DSL_neighbour(board: Board, square: Square) -> Square:
    return board.get_square(square.file - 1, square.rank + 1)


def get_USL_neighbour(board: Board, square: Square) -> Square:
    return board.get_square(square.file - 1, square.rank - 1)


def get_USR_neighbour(board: Board, square: Square) -> Square:
    return board.get_square(square.file + 1, square.rank - 1)


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

    squares: list[Square] = []
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


NeighbourCalculator = Callable[[Board, Square], Square]


def get_neighbour_function(
    piece_type: PieceType,
    colour: Literal[Colour.WHITE, Colour.BLACK],
    move_category: Literal[MoveCategory.CAPTURE, MoveCategory.REGULAR],
) -> list[NeighbourCalculator]:
    if piece_type == PieceType.PAWN:
        if move_category == MoveCategory.REGULAR:
            return [get_US_neighbour] if colour == Colour.WHITE else [get_DS_neighbour]
        if move_category == MoveCategory.CAPTURE:
            return (
                [get_USR_neighbour, get_USL_neighbour]
                if colour == Colour.WHITE
                else [get_DSR_neighbour, get_DSL_neighbour]
            )

    else:
        return PIECE_MOVEMENT[piece_type]


PIECE_MOVEMENT: dict[PieceType, list[NeighbourCalculator]] = {
    PieceType.BISHOP: [
        get_DSL_neighbour,
        get_DSR_neighbour,
        get_USR_neighbour,
        get_USL_neighbour,
    ],
    PieceType.ROOK: [
        get_SL_neighbour,
        get_SR_neighbour,
        get_US_neighbour,
        get_DS_neighbour,
    ],
    PieceType.QUEEN: [
        get_SL_neighbour,
        get_SR_neighbour,
        get_US_neighbour,
        get_DS_neighbour,
        get_DSL_neighbour,
        get_DSR_neighbour,
        get_USR_neighbour,
        get_USL_neighbour,
    ],
    PieceType.KING: [
        get_SL_neighbour,
        get_SR_neighbour,
        get_US_neighbour,
        get_DS_neighbour,
        get_DSL_neighbour,
        get_DSR_neighbour,
        get_USR_neighbour,
        get_USL_neighbour,
    ],
}
