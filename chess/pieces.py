from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from chess.utils import Colour


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

PIECE_VALUE: dict[PieceType, int] = {
    PieceType.EMPTY: 0,
    PieceType.PAWN: 1,
    PieceType.ROOK: 5,
    PieceType.BISHOP: 3,
    PieceType.QUEEN: 9,
    PieceType.KING: 100,
    PieceType.KNIGHT: 3,
}


@dataclass
class Piece:
    colour: Colour = Colour.BLANK
    type: PieceType = PieceType.EMPTY
    orientation: list[Colour] = field(default_factory=list)
    move_limit: int = 7
    capture_limit: int = 7
    moves_made: int = 0
    last_moved: int = 0

    @property
    def has_moved(self) -> bool:
        return self.moves_made > 0

    def move(self) -> None:
        self.moves_made += 1
        if self.type == PieceType.PAWN:
            self.move_limit = 1

    def undo(self):
        self.moves_made -= 1
        if self.type == PieceType.PAWN and self.moves_made == 0:
            self.move_limit = 2

    def promote_to(self, piece: PieceType) -> None:
        self.type = piece

    @staticmethod
    def from_fen(fen: str) -> Piece:
        colour = Colour.WHITE if fen.islower() else Colour.BLACK
        type = FEN_MAP[fen.lower()]
        orientation = (
            [colour] if type == PieceType.PAWN else [Colour.WHITE, Colour.BLACK]
        )
        if type == PieceType.PAWN:
            move_limit = 2
        elif type == PieceType.KING:
            move_limit = 1
        else:
            move_limit = 7
        capture_limit = 1 if type == PieceType.PAWN or type == PieceType.KING else 7
        return Piece(colour, type, orientation, move_limit, capture_limit)

    def __str__(self):
        return PIECE_STR[self.type][self.colour.value]


if __name__ == "__main__":
    pass
