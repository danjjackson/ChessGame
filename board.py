from __future__ import annotations

from dataclasses import dataclass, field
from functools import partial
from typing import Callable

from pieces import Colour, Piece, PieceType
from square import Square

Position = tuple[str, str]
Grid = dict[Position, Square]

notation_map = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}


def empty_board() -> Grid:
    grid: Grid = {}
    for file in "abcdefgh":
        for rank in "12345678":
            grid[(file, rank)] = Square(file, rank)
    return grid


@dataclass
class Board:
    squares: Grid = field(default_factory=empty_board)
    orientation: Colour = Colour.WHITE

    @staticmethod
    def from_fen(
        fen: str = "rnbqk2r/pppppppp/8/8/8/8/PPPPPPPP/RNBQK2R",
        turn: Colour = Colour.WHITE,
    ) -> Board:
        board = Board(orientation=turn)
        fenlist = fen.split("/")

        for ind_rank, rank in enumerate(fenlist):
            column = 0
            for ind_file, char in enumerate(rank):
                if char.isnumeric():
                    column += int(char) - 1
                    continue
                board.place(
                    notation_map[ind_file + column],
                    str(ind_rank + 1),
                    Piece.from_fen(char),
                )
            if column + ind_file != 7:
                raise ValueError("Invalid FEN string")
            column = 0
        return board

    def place(self, file: str, rank: str, piece: Piece):
        self.squares[(file, rank)].piece = piece

    def piece(self, file: str, rank: str) -> Piece:
        return self.squares[(file, rank)].piece

    def empty(self, file: str, rank: str) -> None:
        self.squares[(file, rank)] = Square(file, rank)

    def is_empty(self, file: str, rank: str) -> bool:
        return self.squares[(file, rank)].is_empty

    def find_king(self, colour: Colour) -> Square:
        return self.find_pieces(PieceType.KING, colour)[0]

    def find_pieces(self, piece_type: PieceType, colour: Colour) -> list[Square]:
        squares = []
        for square in self.squares.values():
            if square.piece.type == piece_type and square.piece.colour == colour:
                squares.append(square)

        return squares

    def __str__(self):
        board_repr = ""
        if self.orientation == Colour.WHITE:
            for rank in "87654321":
                for file in "abcdefgh":
                    board_repr = (
                        board_repr + f"| {str(self.squares[(file, rank)].piece)} "
                    )
                board_repr = board_repr + "|\n  _   _   _   _   _   _   _   _\n"
        else:
            for rank in "12345678":
                for file in "hgfedcba":
                    board_repr = (
                        board_repr + f"| {str(self.squares[(file, rank)].piece)} "
                    )
                board_repr = board_repr + "|\n  _   _   _   _   _   _   _   _\n"

        return board_repr


# ValidMoveCalculator = Callable[[Board, int, int], list[Position]]

# MOVE_LISTS: dict[PieceType, list[ValidMoveCalculator]] = {
#     PieceType.ROOK: [get_valid_horizontal_moves, get_valid_vertical_moves],
#     PieceType.BISHOP: [get_valid_diagonal_moves],
#     PieceType.QUEEN: [
#         get_valid_diagonal_moves,
#         get_valid_vertical_moves,
#         get_valid_horizontal_moves,
#     ],
#     PieceType.KNIGHT: [get_valid_knight_moves],
#     PieceType.KING: [
#         partial(get_valid_diagonal_moves, limit=1),
#         partial(get_valid_vertical_moves, limit=1),
#         partial(get_valid_horizontal_moves, limit=1),
#     ],
#     PieceType.PAWN: [partial(get_valid_vertical_moves, limit=2)],
# }

if __name__ == "__main__":
    board = Board.from_fen()
    print(board)
