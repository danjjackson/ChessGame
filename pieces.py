from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum

from moves import (
    Colour,
    Diagonal,
    Horizontal,
    Knight,
    LongCastle,
    MoveType,
    ShortCastle,
    Vertical,
)

Position = tuple[int, int]


class PieceType(Enum):
    EMPTY = "empty"
    PAWN = "pawn"
    ROOK = "rook"
    BISHOP = "bishop"
    QUEEN = "queen"
    KNIGHT = "knight"
    KING = "king"


PIECE_STR: dict[PieceType, tuple[str, str]] = {
    PieceType.EMPTY: (" ", " "),
    PieceType.PAWN: ("♟", "♙"),
    PieceType.ROOK: ("♜", "♖"),
    PieceType.BISHOP: ("♝", "♗"),
    PieceType.QUEEN: ("♛", "♕"),
    PieceType.KING: ("♚", "♔"),
    PieceType.KNIGHT: ("♞", "♘"),
}

FEN_MAP: dict[str, PieceType] = {
    "p": PieceType.PAWN,
    "r": PieceType.ROOK,
    "b": PieceType.BISHOP,
    "q": PieceType.QUEEN,
    "k": PieceType.KING,
    "n": PieceType.KNIGHT,
}


FEN_MOVE_MAP: dict[str, dict[str, list[MoveType]]] = {
    "p": {
        "regular": [Vertical(limit=2, orientation=Colour.WHITE)],
        "capture": [Diagonal(limit=1, orientation=Colour.WHITE)],
    },
    "r": {"regular": [Vertical(), Horizontal()], "capture": [Vertical(), Horizontal()]},
    "b": {"regular": [Diagonal()], "capture": [Diagonal()]},
    "n": {"regular": [Knight()], "capture": [Knight()]},
    "q": {
        "regular": [Vertical(), Horizontal(), Diagonal()],
        "capture": [Vertical(), Horizontal(), Diagonal()],
    },
    "k": {
        "regular": [Vertical(limit=1), Horizontal(limit=1), Diagonal(limit=1)],
        "capture": [Vertical(limit=1), Horizontal(limit=1), Diagonal(limit=1)],
        "short_castle": [ShortCastle()],
        "long_castle": [LongCastle()],
    },
    "P": {
        "regular": [Vertical(limit=2, orientation=Colour.BLACK)],
        "capture": [Diagonal(limit=1, orientation=Colour.BLACK)],
    },
    "R": {"regular": [Vertical(), Horizontal()], "capture": [Vertical(), Horizontal()]},
    "B": {"regular": [Diagonal()], "capture": [Diagonal()]},
    "N": {"regular": [Knight()], "capture": [Knight()]},
    "Q": {
        "regular": [Vertical(), Horizontal(), Diagonal()],
        "capture": [Vertical(), Horizontal(), Diagonal()],
    },
    "K": {
        "regular": [Vertical(limit=1), Horizontal(limit=1), Diagonal(limit=1)],
        "capture": [Vertical(limit=1), Horizontal(limit=1), Diagonal(limit=1)],
        "short_castle": [ShortCastle()],
        "long_castle": [LongCastle()],
    },
}


@dataclass
class Piece:
    x: int
    y: int
    move_type: dict[str, list[MoveType]] = field(default_factory=dict)
    colour: Colour = Colour.BLANK
    type: PieceType = PieceType.EMPTY
    has_moved: bool = False
    moves_made: int = 0
    last_moved: int = 0

    def move_to(self, x: int, y: int) -> None:
        self.x, self.y = x, y
        self.has_moved = True
        self.moves_made += 1
        if self.type == PieceType.PAWN:
            for move_type in self.move_type["regular"]:
                move_type.limit = 1

    def promote_to(self, piece: PieceType) -> None:
        self.type = piece

    @staticmethod
    def from_fen(x: int, y: int, fen: str) -> Piece:
        colour = Colour.WHITE if fen.islower() else Colour.BLACK
        return Piece(
            x, y, deepcopy(FEN_MOVE_MAP[fen]), colour, type=FEN_MAP[fen.lower()]
        )

    def __str__(self):
        return PIECE_STR[self.type][self.colour.value]


if __name__ == "__main__":
    pass