from enum import Enum, StrEnum, auto

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


class PieceType(Enum):
    EMPTY = "empty"
    PAWN = "pawn"
    ROOK = "rook"
    BISHOP = "bishop"
    QUEEN = "queen"
    KNIGHT = "knight"
    KING = "king"
