from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Optional

import pydantic

from pieces import FEN_MAP, Colour, PieceType

Position = tuple[int, int]
notation_map = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}


class MoveCategory(StrEnum):
    REGULAR = auto()
    CAPTURE = auto()
    SHORT_CASTLE = auto()
    LONG_CASTLE = auto()


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


# @dataclass
class Move(pydantic.BaseModel):
    # move: str
    piece: PieceType
    dest: Position
    move_category: MoveCategory
    src: Optional[str | int] = 0


# @staticmethod
def parse_move(player: Colour) -> Move:
    move = input()

    # self.validate_move(move)

    if move[1] == "x":
        move_category = MoveCategory.CAPTURE
    elif move == "0-0":
        return Move(
            # move=move,
            piece=PieceType.KING,
            dest=(0, 6) if player == Colour.WHITE else (7, 6),
            move_category=MoveCategory.SHORT_CASTLE,
        )
    elif move == "0-0-0":
        return Move(
            piece=PieceType.KING,
            dest=(0, 2) if player == Colour.WHITE else (7, 2),
            move_category=MoveCategory.LONG_CASTLE,
        )
    else:
        move_category = MoveCategory.REGULAR

    if move[0].isupper():
        selected_piece_type = FEN_MAP[move[0].lower()]
    else:
        selected_piece_type = FEN_MAP["p"]

    dest = (int(move[-1]) - 1, notation_map[move[-2]])

    return Move(piece=selected_piece_type, dest=dest, move_category=move_category)
