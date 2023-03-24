from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

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
    type: PieceType
    colour: Colour
    move_limit: dict[MoveCategory, int]
    moves_made: int = 0
    last_moved: bool = False

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
        type = FEN_MAP[fen.lower()]
        colour = Colour.WHITE if fen.islower() else Colour.BLACK

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
        return Piece(type, colour, move_limit)

    def __str__(self):
        return PIECE_STR[self.type][self.colour.value]

    @staticmethod
    def make_empty_piece() -> Piece:
        return Piece(
            PieceType.EMPTY,
            Colour.BLANK,
            move_limit={
                MoveCategory.CAPTURE: 7,
                MoveCategory.REGULAR: 7,
            },
        )


if __name__ == "__main__":
    pass
