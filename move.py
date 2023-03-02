from __future__ import annotations

from dataclasses import dataclass

from board import Board
from pieces import FEN_MAP, PieceType
from square import Square
from utils import Colour, MoveCategory

Position = tuple[int, int]
notation_map = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}


checks = ["+", "#"]
possible_moves = [
    "0-0-0",
    "0-0",
    "Nf3",
    "Nxf3",
    "Nbc3",
    "Nbxc3",
    "e4",
    "exd5",
    "e8=Q",
    "exf8=Q",
]


# check if the last symbol is a + or a #, then remove
# Check that the string is under 5 characters
# Deal with castling
# Find piece type
def validation(move):
    if move == "0-0" or move == "0-0-0":
        validate_castling()

    elif move[0] in ["N", "B", "R", "Q", "K"]:
        validate_piece_move(move)

    elif move[0] in ["a", "b", "c", "d", "e", "f", "g", "h"]:
        validate_pawn_move()

    else:
        raise IllegalMoveError


def validate_piece_move(move):
    if len(move) not in [3, 4, 5]:
        raise IllegalMoveError

    cols = ["a", "b", "c", "d", "e", "f", "g", "h"]

    selected_piece_type = FEN_MAP[move[0].lower()]

    if move[-3] == "x":
        move_category = MoveCategory.CAPTURE

    dest = (int(move[-1]) - 1, notation_map[move[-2]])

    if len(move) > 3 and (
        (move[1] in cols and move[2] in cols) or (move[1] in cols and move[3] in cols)
    ):
        source = move[1]

    return


# class MoveValidator(pydantic.BaseModel):


@dataclass
class Move:
    piece_type: PieceType
    dest: Square
    move_category: MoveCategory
    src_file: str = "abcdefgh"
    src_rank: str = "12345678"


def parse_move(board: Board, player: Colour) -> list[Move]:
    move = input()

    if move[1] == "x":
        move_category = MoveCategory.CAPTURE
    elif move == "0-0":
        return [
            Move(
                piece_type=PieceType.KING,
                dest=board.squares[("g", "1")]
                if player == Colour.WHITE
                else board.squares[("g", "8")],
                move_category=MoveCategory.SHORT_CASTLE,
            ),
            Move(
                piece_type=PieceType.ROOK,
                dest=board.squares[("f", "1")]
                if player == Colour.WHITE
                else board.squares[("f", "8")],
                move_category=MoveCategory.SHORT_CASTLE,
                src_file="h",
                src_rank="1" if player == Colour.WHITE else "8",
            ),
        ]
    elif move == "0-0-0":
        return [
            Move(
                piece_type=PieceType.KING,
                dest=board.squares[("c", "1")]
                if player == Colour.WHITE
                else board.squares[("c", "8")],
                move_category=MoveCategory.SHORT_CASTLE,
            ),
            Move(
                piece_type=PieceType.ROOK,
                dest=board.squares[("d", "1")]
                if player == Colour.WHITE
                else board.squares[("d", "8")],
                move_category=MoveCategory.SHORT_CASTLE,
                src_file="a",
                src_rank="1" if player == Colour.WHITE else "8",
            ),
        ]
    else:
        move_category = MoveCategory.REGULAR

    if move[0].isupper():
        selected_piece_type = FEN_MAP[move[0].lower()]
    else:
        selected_piece_type = FEN_MAP["p"]

    dest = board.squares[(move[-2], move[-1])]

    return [
        Move(piece_type=selected_piece_type, dest=dest, move_category=move_category)
    ]
