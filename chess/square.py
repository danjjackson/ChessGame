from __future__ import annotations

from dataclasses import dataclass, field

from chess.pieces import Piece, PieceType

int_str_file_map = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
int_str_rank_map = {0: "1", 1: "2", 2: "3", 3: "4", 4: "5", 5: "6", 6: "7", 7: "8"}


@dataclass
class Square:
    file: int = 0
    rank: int = 0
    piece: Piece = field(default_factory=Piece)

    @property
    def is_empty(self) -> bool:
        return self.piece.type == PieceType.EMPTY

    def empty(self) -> None:
        self.piece.type = PieceType.EMPTY

    def set_piece(self, piece: Piece) -> None:
        self.piece = piece

    def move_piece(self, destination: Square, undo: bool = False):
        piece = self.piece
        piece.move() if not undo else piece.undo()
        destination.piece = piece

        self.piece = Piece()

    def __str__(self):
        return (
            f"{int_str_file_map[self.file]}{int_str_rank_map[self.rank]} is empty"
            if self.piece.type == PieceType.EMPTY
            else f"There is a {str(self.piece)} on {int_str_file_map[self.file]}{int_str_rank_map[self.rank]}"
        )
