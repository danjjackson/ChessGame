from __future__ import annotations

from dataclasses import dataclass, field
from functools import partial
from typing import Callable

from pieces import Colour, Piece, PieceType
from square import Square

Position = tuple[int, int]
Grid = dict[Position, Square]


def empty_board() -> Grid:
    grid: Grid = {}
    for x in range(8):
        for y in range(8):
            grid[(x, y)] = Square()
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

        for ind_row, row in enumerate(fenlist):
            column = 0
            for ind_col, char in enumerate(row):
                if char.isnumeric():
                    column += int(char) - 1
                    continue
                board.place(Piece.from_fen(ind_row, ind_col + column, char))
            if column + ind_col != 7:
                raise ValueError("Invalid FEN string")
            column = 0
        return board

    def place(self, x: int, y: int, piece: Piece):
        self.squares[(x, y)].piece = piece

    def piece(self, x: int, y: int) -> Piece:
        return self.squares[(x, y)].piece

    def empty(self, x: int, y: int) -> None:
        self.squares[(x, y)] = Square(x, y)

    def is_empty(self, x: int, y: int) -> bool:
        return self.piece(x, y).type == PieceType.EMPTY

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
            for x in range(7, -1, -1):
                for y in range(8):
                    board_repr = board_repr + f"| {str(self.squares[(x, y)].piece)} "
                board_repr = board_repr + "|\n  _   _   _   _   _   _   _   _\n"
        else:
            for x in range(8):
                for y in range(7, -1, -1):
                    board_repr = board_repr + f"| {str(self.squares[(x, y)].piece)} "
                board_repr = board_repr + "|\n  _   _   _   _   _   _   _   _\n"

        return board_repr


ValidMoveCalculator = Callable[[Board, int, int], list[Position]]

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
