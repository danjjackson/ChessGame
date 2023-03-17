from dataclasses import dataclass, field

from chess.board import Board
from chess.moves import MoveCategory
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
            piece for piece in self.pieces_captured if piece.type != PieceType.EMPTY
        ]
        self.pieces_captured.sort(
            key=lambda piece: PIECE_VALUE[piece.type], reverse=True
        )

    def __str__(self):
        self.clean_pieces_captured_list()
        return f"{self.first_name} {self.last_name} ({self.rating})" + (
            " {}" * len(self.pieces_captured)
        ).format(*self.pieces_captured)

    def king_is_in_check(self, board: Board) -> bool:
        king_square = board.find_king(self.colour)

        is_in_check = False

        for square in board.squares.values():
            if (
                square.piece.colour != self.colour
                and square.piece.type != PieceType.EMPTY
            ):
                if board.is_reachable(square, king_square, MoveCategory.CAPTURE):
                    is_in_check = True

        return is_in_check
