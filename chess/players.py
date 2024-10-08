from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from chess.pieces import Piece, PieceType
from chess.utils import Colour

PIECE_VALUE: dict[PieceType, int] = {
    PieceType.EMPTY: 0,
    PieceType.PAWN: 1,
    PieceType.ROOK: 5,
    PieceType.BISHOP: 3,
    PieceType.QUEEN: 9,
    PieceType.KNIGHT: 3,
}


@dataclass
class Player:
    name: str
    rating: int
    colour: Literal[Colour.WHITE, Colour.BLACK] = Colour.WHITE
    pieces_captured: list[Piece] = field(default_factory=list)

    def clean_pieces_captured_list(self):
        self.pieces_captured = [
            piece for piece in self.pieces_captured if piece != None
        ]
        self.pieces_captured.sort(
            key=lambda piece: PIECE_VALUE[piece.type], reverse=True
        )

    def __str__(self):
        self.clean_pieces_captured_list()
        return f"{self.name} ({self.rating})" + (
            " {}" * len(self.pieces_captured)
        ).format(*self.pieces_captured)
