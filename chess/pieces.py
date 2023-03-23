from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from chess.utils import Colour, MoveCategory


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


@dataclass
class Piece:
    colour: Colour = Colour.BLANK
    type: PieceType = PieceType.EMPTY
    move_limit: dict[MoveCategory, int] = {
        MoveCategory.CAPTURE: 7,
        MoveCategory.REGULAR: 7,
    }
    moves_made: int = 0
    last_moved: bool = False
    direction: Optional[Colour] = None

    @property
    def has_moved(self) -> bool:
        return self.moves_made > 0

    def move(self) -> None:
        self.moves_made += 1
        self.last_moved = True
        if self.type == PieceType.PAWN:
            self.move_limit[MoveCategory.REGULAR] = 1

    def undo(self):
        self.moves_made -= 1
        self.last_moved = False
        if self.type == PieceType.PAWN and self.moves_made == 0:
            self.move_limit[MoveCategory.REGULAR] = 2

    def promote_to(self, piece_type: PieceType) -> None:
        self.type = piece_type

    @staticmethod
    def from_fen(fen: str) -> Piece:
        colour = Colour.WHITE if fen.islower() else Colour.BLACK
        type = FEN_MAP[fen.lower()]
        orientation = (
            [colour] if type == PieceType.PAWN else [Colour.WHITE, Colour.BLACK]
        )
        if type == PieceType.PAWN:
            move_limit = {
                MoveCategory.CAPTURE: 1,
                MoveCategory.REGULAR: 2,
            }
        elif type == PieceType.KING:
            move_limit = {
                MoveCategory.CAPTURE: 1,
                MoveCategory.REGULAR: 1,
            }
        else:
            move_limit = {
                MoveCategory.CAPTURE: 7,
                MoveCategory.REGULAR: 7,
            }
        return Piece(colour, type, move_limit)

    def __str__(self):
        return PIECE_STR[self.type][self.colour.value]


if __name__ == "__main__":
    pass
