from __future__ import annotations

from dataclasses import dataclass, field

from pieces import Piece, PieceType


@dataclass
class Square:
    file: str = ""
    rank: str = ""
    piece: Piece = field(default_factory=Piece)

    @property
    def is_empty(self) -> bool:
        return self.piece.type == PieceType.EMPTY

    def move_piece(self, destination: Square, undo: bool = False):
        piece = self.piece
        piece.move() if not undo else piece.undo()
        destination.piece = piece

        self.piece = Piece()

    def __str__(self):
        return f"There is a {str(self.piece)} on {self.file}{self.rank}"
