from __future__ import annotations

from dataclasses import dataclass, field
from typing import Self

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
    first_name: str
    last_name: str
    rating: int
    colour: Colour = Colour.WHITE
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
        return f"{self.first_name} {self.last_name} ({self.rating})" + (
            " {}" * len(self.pieces_captured)
        ).format(*self.pieces_captured)

    @staticmethod
    def make_player(colour: Colour) -> Player:
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        rating = int(input("Enter your rating: "))

        return Player(first_name, last_name, rating, colour)
