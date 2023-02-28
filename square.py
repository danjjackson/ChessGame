from __future__ import annotations

from dataclasses import dataclass

from pieces import Piece, PieceType


@dataclass
class Square:
    rank: str
    file: str
    piece: Piece = Piece()

    @property
    def is_empty(self) -> bool:
        return self.piece.type == PieceType.EMPTY

    def move_piece(self, destination: Square):
        piece = self.piece
        piece.move()
        destination.piece = piece

        self.piece = Piece()
